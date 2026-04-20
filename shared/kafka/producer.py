import json
import logging
from aiokafka import AIOKafkaProducer

logger = logging.getLogger(__name__)

class KafkaProducerManager:
    def __init__(self, bootstrap_servers: str):
        self.bootstrap_servers = bootstrap_servers
        self._producer = None

    async def start(self):
        self._producer = AIOKafkaProducer(
            bootstrap_servers=self.bootstrap_servers,
            value_serializer=lambda v: json.dumps(v, default=str).encode('utf-8')
        )
        await self._producer.start()
        logger.info(f"Kafka Producer started at {self.bootstrap_servers}")

    async def stop(self):
        if self._producer:
            await self._producer.stop()
            logger.info("Kafka Producer stopped")

    async def publish(self, topic: str, event: dict):
        if not self._producer:
            raise RuntimeError("Producer not started")
        await self._producer.send_and_wait(topic, event)
        logger.debug(f"Published event to {topic}")
