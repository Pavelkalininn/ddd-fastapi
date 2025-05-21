from typing import Optional
from sqlalchemy import select, not_
from sqlalchemy.ext.asyncio import AsyncSession

from delivery_core.domain.model.order_aggregate.order import Order
from delivery_core.domain.model.order_aggregate.order_status import OrderStatus
from .get_not_completed_orders_query import GetNotCompletedOrdersQuery
from .get_not_completed_orders_response import GetNotCompletedOrdersResponse, \
    LocationResponse, OrderResponse


class GetNotCompletedOrdersHandler:
    """Обработчик запроса незавершенных заказов"""

    def __init__(self, session: AsyncSession):
        self._session = session

    async def handle(self, query: GetNotCompletedOrdersQuery) -> Optional[
        GetNotCompletedOrdersResponse]:
        """Обработать запрос"""
        stmt = select(Order).where(
            not_(Order.status == OrderStatus.completed())
        )

        result = await self._session.execute(stmt)
        db_orders = result.scalars().all()

        if not db_orders:
            return None

        orders = [
            OrderResponse(
                id=order.id,
                location=LocationResponse(
                    x=order.location_x,
                    y=order.location_y
                ),
                status=order.status
            )
            for order in db_orders
        ]

        return GetNotCompletedOrdersResponse(orders=orders)