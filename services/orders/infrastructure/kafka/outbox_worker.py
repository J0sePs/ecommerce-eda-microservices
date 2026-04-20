import asyncio
import logging
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from core.database import SessionLocal
from infrastructure.db.models import OutboxModel
from shared.kafka.producer import KafkaProducerManager
from core.config import settings

logger = logging.getLogger(__name__)

class OutboxWorker:
    def __init__(self, producer: KafkaProducerManager):
        self.producer = producer
        self._running = False

    async def start(self):
        self._running = True
        logger.info("Outbox worker starting...")
        while self._running:
            try:
                await self._process_outbox()
            except Exception as e:
                logger.error(f"Error processing outbox: {e}")
            await asyncio.sleep(2)

    async def stop(self):
        self._running = False
        logger.info("Outbox worker stopping...")

    async def _process_outbox(self):
        async with SessionLocal() as session:
            stmt = select(OutboxModel).where(OutboxModel.published == False).order_by(OutboxModel.created_at).limit(50)
            result = await session.execute(stmt)
            events = result.scalars().all()

            if not events:
                return

            for event in events:
                topic = event.event_type
                payload = event.payload
                try:
                    await self.producer.publish(topic, payload)
                    event.published = True
                    event.published_at = datetime.utcnow()
                except Exception as e:
                    logger.error(f"Failed to publish event {event.id}: {e}")
                    event.retries += 1
            
            await session.commit()
