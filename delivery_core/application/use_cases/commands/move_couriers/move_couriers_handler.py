from typing import List, Optional
from dataclasses import dataclass

from delivery_core.application.use_cases.commands.move_couriers.move_couriers_command import \
    MoveCouriersCommand
from delivery_core.domain.model.courier_aggregate.courier import Courier
from delivery_core.domain.model.order_aggregate.order import Order
from delivery_core.ports.i_courier_repository import ICourierRepository
from delivery_core.ports.i_order_repository import IOrderRepository
from delivery_other.general_errors import Error
from delivery_other.i_unit_of_work import IUnitOfWork
from delivery_other.primitives import Result


@dataclass
class MoveCouriersHandler:
    """Обработчик перемещения курьеров"""
    _unit_of_work: IUnitOfWork
    _order_repo: IOrderRepository
    _courier_repo: ICourierRepository

    async def handle(self, command: MoveCouriersCommand) -> Result[None, Error]:
        """Обработать команду перемещения"""
        # Получаем назначенные заказы
        assigned_orders: List[Order] = self._order_repo.get_all_in_assigned_status()
        if not assigned_orders:
            return Result.success()

        # Обрабатываем каждый заказ
        for order in assigned_orders:
            if not order.courier_id:
                return Result.fail(Error(
                    code="invalid_order",
                    message="У заказа отсутствует курьер"
                ))

            # Получаем курьера
            courier: Optional[Courier] = await self._courier_repo.get_async(order.courier_id)
            if not courier:
                return Result.fail(Error(
                    code="invalid_courier",
                    message=f"Курьер {order.courier_id} не найден"
                ))

            # Перемещаем курьера
            move_result = courier.move(order.location)
            if not move_result.is_success:
                return move_result

            # Проверяем достижение точки
            if order.location == courier.location:
                order.complete()
                courier.set_free()

            # Обновляем данные
            self._courier_repo.update(courier)
            self._order_repo.update(order)

        # Сохраняем изменения
        await self._unit_of_work.commit()
        return Result.success()