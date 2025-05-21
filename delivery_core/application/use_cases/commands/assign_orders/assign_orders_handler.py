from dataclasses import dataclass

from delivery_core.application.use_cases.commands.assign_orders.assign_orders_command import \
    AssignOrdersCommand
from delivery_core.domain.services.i_dispatch_service import IDispatchService
from delivery_core.ports.i_courier_repository import ICourierRepository
from delivery_core.ports.i_order_repository import IOrderRepository
from delivery_other.general_errors import Error
from delivery_other.i_unit_of_work import IUnitOfWork
from delivery_other.primitives import Result


@dataclass
class AssignOrdersHandler:
    """Обработчик команды массового назначения"""
    _unit_of_work: IUnitOfWork
    _order_repo: IOrderRepository
    _courier_repo: ICourierRepository
    _dispatch_service: IDispatchService

    async def handle(self, command: AssignOrdersCommand) -> Result[
        None, Error]:
        """Обработать команду"""
        order = await self._order_repo.get_first_in_created_status()
        if not order:
            return Result.failure(Error(
                code="not_available_orders",
                message="Нет заказов для назначения"
            ))

        free_couriers = self._courier_repo.get_all_in_free_status()
        if not free_couriers:
            return Result.failure(Error(
                code="not_available_couriers",
                message="Нет доступных курьеров"
            ))

        dispatch_result = self._dispatch_service.dispatch(order, free_couriers)
        if not dispatch_result.is_success:
            return dispatch_result

        courier = dispatch_result.value
        self._courier_repo.update(courier)
        self._order_repo.update(order)

        await self._unit_of_work.commit()
        return Result.success()
