from abc import ABC, abstractmethod
from typing import List, Optional

class IOrderRepository(ABC):
    @abstractmethod
    async def create(self, order) -> None:
        pass
    
    @abstractmethod
    async def get_by_id(self, order_id: str):
        pass

class IEventBus(ABC):
    @abstractmethod
    async def publish(self, topic: str, event: dict) -> None:
        pass
