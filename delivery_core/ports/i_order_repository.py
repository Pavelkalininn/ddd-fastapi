from typing import Protocol, Optional, Iterable
import uuid

from delivery_core.domain.model.order_aggregate.order import Order


class IOrderRepository(Protocol):
    """Repository interface for Order Aggregate"""

    async def add_async(self, order: Order) -> Order:
        """
        Add a new order

        Args:
            order: Order to add

        Returns:
            The added order
        """
        ...

    def update(self, order: Order) -> None:
        """
        Update an existing order

        Args:
            order: Order to update
        """
        ...

    async def get_async(self, order_id: uuid.UUID) -> Optional[Order]:
        """
        Get order by ID

        Args:
            order_id: Order identifier

        Returns:
            Maybe[Order]: Order if found, None otherwise
        """
        ...

    async def get_first_in_created_status_async(self) -> Optional[Order]:
        """
        Get the first order with created status

        Returns:
            Maybe[Order]: First created order if exists
        """
        ...

    def get_all_in_assigned_status(self) -> Iterable[Order]:
        """
        Get all orders with assigned status

        Returns:
            Iterable collection of assigned orders
        """
        ...