import uuid
from datetime import datetime
from typing import Generic, TypeVar, Optional
from pydantic import BaseModel, Field

T = TypeVar('T', bound=BaseModel)

class EventMetadata(BaseModel):
    correlation_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    causation_id: Optional[str] = None

class BaseEventEnvelope(BaseModel, Generic[T]):
    event_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    event_type: str
    version: str = "1.0"
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    source: str
    payload: T
    metadata: EventMetadata = Field(default_factory=EventMetadata)
