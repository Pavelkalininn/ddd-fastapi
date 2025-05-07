import uuid
from dataclasses import dataclass
from typing import Optional

from delivery_core.domain.model.courier_aggregate.courier import Courier
from delivery_core.domain.model.order_aggregate.order_status import OrderStatus
from delivery_core.domain.shared_kernel.location import Location
from delivery_other.general_errors import Error, GeneralErrors
from delivery_other.primitives import Result, UnitResult


@dataclass
class Order:
    def __init__(self, order_id: uuid.UUID, location: Location):
        self._id = order_id
        self._location = location
        self._status = OrderStatus.created().name
        self._courier_id: Optional[uuid.UUID] = None

    @property
    def id(self) -> uuid.UUID:
        return self._id

    @property
    def courier_id(self) -> Optional[uuid.UUID]:
        return self._courier_id

    @property
    def location(self) -> Location:
        return self._location

    @property
    def status(self) -> str:
        return self._status

    @staticmethod
    def create(order_id: uuid.UUID, location: Location) -> Result['Order', Error]:
        if order_id == uuid.UUID(int=0):
            return Result.failure(GeneralErrors.value_is_required("order_id"))
        if not location:
            return Result.failure(GeneralErrors.value_is_required("location"))
        return Result.success(Order(order_id, location))

    def assign(self, courier: Courier) -> UnitResult[Error]:
        if not courier:
            return UnitResult.failure(GeneralErrors.value_is_required("courier"))
        if self._status != OrderStatus.created().name:
            return UnitResult.failure(OrderErrors.cant_assign_already_assigned_order(courier.id))

        self._courier_id = courier.id
        self._status = OrderStatus.assigned().name
        return UnitResult.success()

    def complete(self) -> UnitResult[Error]:
        if self._status != OrderStatus.assigned().name:
            return UnitResult.failure(OrderErrors.cant_complete_not_assigned_order())

        self._status = OrderStatus.completed().name
        return UnitResult.success()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Order):
            return False
        return self._id == other._id

    def __hash__(self) -> int:
        return hash(self._id)


from dataclasses import dataclass
import uuid

@dataclass
class OrderErrors:
    @staticmethod
    def cant_complete_not_assigned_order() -> 'Error':
        return Error(
            code="order.cant.complete.not.assigned.order",
            message="Нельзя завершить заказ, который не был назначен"
        )

    @staticmethod
    def cant_assign_order_to_busy_courier(courier_id: uuid.UUID) -> 'Error':
        return Error(
            code="order.cant.assign.order.to.busy.courier",
            message=f"Нельзя назначить заказ на курьера, который занят. Id курьера = {courier_id}"
        )

    @staticmethod
    def cant_assign_already_assigned_order(courier_id: uuid.UUID) -> 'Error':
        return Error(
            code="order.cant.assign.already.assigned.order",
            message=f"Нельзя назначить уже назначенный заказ {courier_id}"
        )