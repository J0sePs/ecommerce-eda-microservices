import json
import asyncio
import logging
from typing import Callable, Dict, List, Awaitable
from aiokafka import AIOKafkaConsumer, ConsumerRecord
from .producer import KafkaProducerManager

logger = logging.getLogger(__name__)

class KafkaConsumerManager:
    def __init__(self, bootstrap_servers: str, group_id: str, topics: List[str], handlers: Dict[str, List[Callable[[dict], Awaitable[None]]]], dlq_producer: KafkaProducerManager = None):
        self.bootstrap_servers = bootstrap_servers
        self.group_id = group_id
        self.topics = topics
        self.handlers = handlers
        self.max_retries = 3
        self._consumer = None
        self.dlq_producer = dlq_producer

    async def start(self):
        self._consumer = AIOKafkaConsumer(
            *self.topics,
            bootstrap_servers=self.bootstrap_servers,
            group_id=self.group_id,
            enable_auto_commit=False,
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )
        await self._consumer.start()
        logger.info(f"Kafka Consumer started for topics: {self.topics}")

    async def stop(self):
        if self._consumer:
            await self._consumer.stop()
            logger.info("Kafka Consumer stopped")

    async def consume_loop(self):
        if not self._consumer:
            raise RuntimeError("Consumer not started")
        
        try:
            async for msg in self._consumer:
                await self._process_message(msg)
        except asyncio.CancelledError:
            logger.info("Consume loop cancelled")
        except Exception as e:
            logger.error(f"Error in consume loop: {e}")

    async def _process_message(self, msg: ConsumerRecord):
        event = msg.value
        topic = msg.topic
        
        handlers = self.handlers.get(topic, [])
        for handler in handlers:
            try:
                await handler(event)
            except Exception as e:
                logger.error(f"Error processing message on {topic}: {e}")
                await self._handle_failure(topic, event, e)
        
        await self._consumer.commit()

    async def _handle_failure(self, original_topic: str, event: dict, error: Exception):
        logger.warning(f"Handling failure for event on {original_topic}. DLQ process initiating.")
        if self.dlq_producer:
            dlq_topic = f"dlq.{original_topic}"
            dlq_event = {
                "original_topic": original_topic,
                "error": str(error),
                "failed_event": event
            }
            await self.dlq_producer.publish(dlq_topic, dlq_event)
            logger.info(f"Sent failed event to {dlq_topic}")
