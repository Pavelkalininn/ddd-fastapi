from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.job import Job
from dependency_injector.wiring import Provide, inject

from delivery_core.application.use_cases.commands.assign_orders.assign_orders_command import \
    AssignOrdersCommand
from delivery_core.application.use_cases.commands.assign_orders.assign_orders_handler import \
    AssignOrdersHandler


class AssignOrdersJob:
    """Фоновая задача для назначения заказов курьерам"""

    @inject
    def __init__(
            self,
            scheduler: AsyncIOScheduler = Provide["scheduler"],
            assign_orders_handler: AssignOrdersHandler = Provide[
                "assign_orders_handler"]
    ):
        self._scheduler = scheduler
        self._handler = assign_orders_handler

    async def execute(self, job: Job) -> None:
        """Выполнить задачу"""
        command = AssignOrdersCommand()
        await self._handler.handle(command)

    def schedule(self, interval_seconds: int = 60) -> None:
        """Запланировать периодическое выполнение"""
        self._scheduler.add_job(
            self.execute,
            'interval',
            seconds=interval_seconds,
            id='assign_orders_job',
            replace_existing=True
        )