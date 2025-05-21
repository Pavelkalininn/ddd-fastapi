from abc import ABC, abstractmethod
from typing import AsyncContextManager


class IUnitOfWork(AsyncContextManager, ABC, ):
    """Async Unit of Work interface with context manager support"""

    @abstractmethod
    async def commit(self) -> bool:
        ...

    @abstractmethod
    async def rollback(self) -> None:
        ...

    @abstractmethod
    async def __aenter__(self):
        ...

    @abstractmethod
    async def __aexit__(self, exc_type, exc, tb):
        ...