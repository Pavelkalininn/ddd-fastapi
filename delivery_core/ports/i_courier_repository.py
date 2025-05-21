from typing import Protocol, Iterable, Optional
import uuid

from delivery_core.domain.model.courier_aggregate.courier import Courier


class ICourierRepository(Protocol):
    """Repository interface for Courier Aggregate"""

    async def add_async(self, courier: Courier) -> Courier:
        """
        Add a new courier

        Args:
            courier: Courier to add

        Returns:
            The added courier
        """
        ...

    def update(self, courier: Courier) -> None:
        """
        Update an existing courier

        Args:
            courier: Courier to update
        """
        ...

    async def get_async(self, courier_id: uuid.UUID) -> Optional[Courier]:
        """
        Get courier by ID

        Args:
            courier_id: Courier identifier

        Returns:
            Maybe[Courier]: Courier if found, None otherwise
        """
        ...

    def get_all_in_free_status(self) -> Iterable[Courier]:
        """
        Get all couriers with free status

        Returns:
            Iterable collection of free couriers
        """
        ...