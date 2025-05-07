from typing import Optional
import uuid

from delivery_core.domain.model.courier_aggregate.courier_status import \
    CourierStatus
from delivery_core.domain.model.courier_aggregate.transport import Transport
from delivery_core.domain.shared_kernel.location import Location
from delivery_other.general_errors import Error, GeneralErrors
from delivery_other.primitives import Result, UnitResult


class Courier:
    def __init__(self, courier_id: uuid.UUID, name: str, transport: Transport, location: Location):
        self.id = courier_id
        self.name = name
        self.transport = transport
        self.location = location
        self.status = CourierStatus.free
        self.courier_id: Optional[uuid.UUID] = None

    @classmethod
    def create(cls, courier_id: uuid.UUID, name: str, transport: Transport, location: Location) -> Result['Courier', Error]:
        if courier_id == uuid.UUID(int=0):
            return Result.failure(GeneralErrors.value_is_required("courier_id"))
        if not name:
            return Result.failure(GeneralErrors.value_is_required("name"))
        if not location:
            return Result.failure(GeneralErrors.value_is_required("location"))
        if not transport:
            return Result.failure(GeneralErrors.value_is_required("transport"))
        return Result.success(cls(courier_id, name, transport, location))

    def assign(self, courier_id: uuid.UUID) -> UnitResult[Error]:
        if not courier_id:
            return UnitResult.failure(GeneralErrors.value_is_required("courier"))
        if self.status != CourierStatus.free:
            return UnitResult.failure(Errors.cant_assign_order_to_busy_courier(courier_id))

        self.courier_id = courier_id
        self.status = CourierStatus.busy
        return UnitResult.success()

    def complete(self) -> UnitResult[Error]:
        if self.status != CourierStatus.busy:
            return UnitResult.failure(Errors.cant_complete_not_assigned_courier())

        self.status = CourierStatus.free
        return UnitResult.success()

    def get_step_count(self, destination: Location) -> Result[int, Error]:
        distance = self.location.calculate_distance_to(destination)
        return Result.success(distance // self.transport.speed)

    def move(self, target: Location) -> UnitResult[Error]:
        self.location = self.transport.move(self.location, target).value
        return UnitResult.success()

class Errors:
    @staticmethod
    def cant_complete_not_assigned_courier() -> Error:
        return Error(
            code="courier.cant.complete.not.assigned.courier",
            message="Нельзя завершить заказ, который не был назначен"
        )

    @staticmethod
    def cant_assign_order_to_busy_courier(courier_id: uuid.UUID) -> Error:
        return Error(
            code="order.cant.assign.order.to.busy.courier",
            message=f"Нельзя назначить заказ на курьера, который занят. Id курьера = {courier_id}"
        )
