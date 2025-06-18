from dataclasses import dataclass

from delivery_core.domain.model.order_aggregate.order import Order
from delivery_core.domain.shared_kernel.location import Location
from delivery_core.ports.i_order_repository import IOrderRepository
from delivery_infrastructure.adapters.grpc.contract_pb2_grpc import Geo
from delivery_other.general_errors import Error
from delivery_other.i_unit_of_work import IUnitOfWork
from delivery_other.primitives import Result
from .create_order_command import CreateOrderCommand


@dataclass
class CreateOrderHandler:
    """Обработчик команды создания заказа"""
    _unit_of_work: IUnitOfWork
    _order_repo: IOrderRepository
    _geo_client: Geo

    async def handle(self, command: CreateOrderCommand) -> Result[None, Error]:
        """Обработать команду создания заказа"""
        existing_order = await self._order_repo.get_async(command.basket_id)
        if existing_order:
            return Result.success()

        geolocation_result = await self._geo_client.get_geolocation_async(
            command.street)
        if geolocation_result.is_err():
            return geolocation_result
        location = geolocation_result.unwrap()
        order_result = Order.create(command.basket_id, location)
        if not order_result.is_success:
            return order_result
        await self._order_repo.add_async(order_result.value)
        await self._unit_of_work.commit()

        return Result.success()