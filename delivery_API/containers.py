from dependency_injector import containers, providers
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from delivery_API.adapters.background_jobs.assign_order_job import \
    AssignOrdersJob
from delivery_API.adapters.background_jobs.move_couriers_job import \
    MoveCouriersJob


class BackgroundJobsContainer(containers.DeclarativeContainer):
    scheduler = providers.Singleton(AsyncIOScheduler)
    assign_orders_job = providers.Factory(
        AssignOrdersJob,
        scheduler=scheduler,
        assign_orders_handler=providers.Dependency()
    )
    move_couriers_job = providers.Factory(
        MoveCouriersJob,
        scheduler=scheduler,
        move_couriers_handler=providers.Dependency()
    )