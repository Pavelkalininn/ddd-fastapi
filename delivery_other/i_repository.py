from abc import abstractmethod, ABC
from typing import Generic, TypeVar, Optional
import uuid
from delivery_core.domain.model import AggregateRoot

T = TypeVar('T', bound=AggregateRoot)


class IRepository(Generic[T], ABC):
    """Generic repository interface for aggregate roots"""

    @abstractmethod
    async def add_async(self, entity: T) -> None:
        """Add a new entity"""
        ...

    @abstractmethod
    def update(self, entity: T) -> None:
        """Update an existing entity"""
        ...

    @abstractmethod
    async def get_async(self, id: uuid.UUID) -> Optional[T]:
        """Get entity by ID"""
        ...

    @abstractmethod
    def remove(self, entity: T) -> None:
        """Remove an entity"""
        ...