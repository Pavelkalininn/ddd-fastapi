from typing import List, Optional
import uuid
from sqlalchemy.orm import Session

from delivery_core.domain.model.order_aggregate.order import Order
from delivery_core.domain.model.order_aggregate.order_status import OrderStatus
from delivery_core.ports.i_order_repository import IOrderRepository
from delivery_infrastructure.adapters.postgres.entity_configurations.order_aggregate.order_entity_type_configuration import \
    OrderModel


class OrderRepository(IOrderRepository):
    def __init__(self, session: Session):
        self._session = session

    async def add_async(self, order: Order) -> Order:
        order_model = OrderModel.from_domain(order)
        self._session.add(order_model)
        return order

    def update(self, order: Order) -> None:
        order_model = OrderModel.from_domain(order)
        self._session.merge(order_model)

    async def get_async(self, order_id: uuid.UUID) -> Optional[Order]:
        order_model = (
            self._session.query(OrderModel)
            .filter(OrderModel.id == str(order_id))
            .first()
        )
        return order_model.to_domain() if order_model else None

    async def get_first_in_created_status_async(self) -> Optional[Order]:
        order_model = (
            self._session.query(OrderModel)
            .filter(OrderModel.status == OrderStatus.created().name)
            .first()
        )
        return order_model.to_domain() if order_model else None

    def get_all_in_assigned_status(self) -> List[Order]:
        order_models = (
            self._session.query(OrderModel)
            .filter(OrderModel.status == OrderStatus.assigned().name)
            .all()
        )
        return [om.to_domain() for om in order_models]