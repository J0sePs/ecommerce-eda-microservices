import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from core.database import engine, Base
from api.v1.orders import router as orders_router
from core.config import settings
from shared.kafka.producer import KafkaProducerManager
from infrastructure.kafka.outbox_worker import OutboxWorker
import logging

logger = logging.getLogger(__name__)

# Global instances
producer = KafkaProducerManager(bootstrap_servers=settings.KAFKA_URL)
outbox_worker = OutboxWorker(producer)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup Database
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
    # Start Kafka Producer with backoff
    connected = False
    for _ in range(10):
        try:
            await producer.start()
            connected = True
            logger.info("Kafka producer started.")
            break
        except Exception as e:
            logger.warning(f"Waiting for Kafka to be ready... {e}")
            await asyncio.sleep(3)
            
    if not connected:
        logger.error("Could not connect to Kafka after multiple retries. Service might be degraded.")

    # Start Outbox Worker in background
    worker_task = asyncio.create_task(outbox_worker.start())
    logger.info("Outbox Worker background task started.")

    yield
    
    # Shutdown
    logger.info("Shutting down...")
    await outbox_worker.stop()
    await worker_task
    await producer.stop()
    await engine.dispose()

app = FastAPI(title="Orders Service", lifespan=lifespan)
app.include_router(orders_router, prefix="/api/v1/orders", tags=["orders"])
