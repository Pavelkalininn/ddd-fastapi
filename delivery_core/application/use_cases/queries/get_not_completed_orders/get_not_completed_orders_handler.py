from typing import Optional
from sqlalchemy import select, not_
from sqlalchemy.ext.asyncio import AsyncSession

from delivery_core.domain.model.order_aggregate.order import Order
from delivery_core.domain.model.order_aggregate.order_status import OrderStatus
from .get_not_completed_orders_query import GetNotCompletedOrdersQuery
from .get_not_completed_orders_response import GetNotCompletedOrdersResponse, \
    LocationResponse, OrderResponse


class GetNotCompletedOrdersHandler:
    async def handle(self, db: AsyncSession) -> GetNotCompletedOrdersResponse:
        """Получить все незавершенные заказы"""
        stmt = select(Order).where(not_(DbOrder.status == "completed"))
        result = await db.execute(stmt)
        orders = result.scalars().all()

        return GetNotCompletedOrdersResponse(
            orders=[
                OrderResponse(
                    id=order.id,
                    location={"x": order.location_x, "y": order.location_y},
                    status=order.status
                )
                for order in orders
            ]
        )