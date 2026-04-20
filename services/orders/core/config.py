from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "orders-service"
    DATABASE_URL: str = "postgresql+asyncpg://orders_user:orders_pass@postgres-orders:5432/orders_db"
    KAFKA_URL: str = "kafka:29092"
    REDIS_URL: str = "redis://redis:6379/0"
    CORS_ORIGINS: list = ["*"]
    
    class Config:
        env_file = ".env"

settings = Settings()
