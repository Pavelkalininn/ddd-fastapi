from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.job import Job
from dependency_injector.wiring import inject, Provide
import logging

from delivery_core.application.use_cases.commands.move_couriers.move_couriers_command import \
    MoveCouriersCommand
from delivery_core.application.use_cases.commands.move_couriers.move_couriers_handler import \
    MoveCouriersHandler

logger = logging.getLogger(__name__)


class MoveCouriersJob:
    """Фоновая задача для перемещения курьеров"""

    @inject
    def __init__(
            self,
            scheduler: AsyncIOScheduler = Provide["scheduler"],
            move_couriers_handler: MoveCouriersHandler = Provide[
                "move_couriers_handler"]
    ):
        self._scheduler = scheduler
        self._handler = move_couriers_handler

    async def execute(self, job: Job) -> None:
        """Выполнить задачу перемещения курьеров"""
        try:
            command = MoveCouriersCommand()
            result = await self._handler.handle(command)

            if not result.is_success:
                logger.error(f"Move couriers failed: {result.error}")
            else:
                logger.debug("Couriers moved successfully")

        except Exception as e:
            logger.exception("Unhandled exception in MoveCouriersJob")

    def schedule(self, interval_seconds: int = 30) -> None:
        """Запланировать периодическое выполнение"""
        self._scheduler.add_job(
            self.execute,
            'interval',
            seconds=interval_seconds,
            id='move_couriers_job',
            max_instances=1,  # Аналог DisallowConcurrentExecution
            replace_existing=True
        )