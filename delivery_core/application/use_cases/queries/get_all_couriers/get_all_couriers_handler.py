from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result

from .get_all_couriers_query import GetAllCouriersQuery
from .get_all_couriers_response import CourierResponse, GetAllCouriersResponse, \
    Location
from ...infrastructure.database import models as db_models


class GetAllCouriersHandler:
    """Обработчик запроса всех курьеров"""

    def __init__(self, session: AsyncSession):
        self._session = session

    async def handle(self, query: GetAllCouriersQuery) -> Optional[
        GetAllCouriersResponse]:
        """Обработать запрос"""
        stmt = select(db_models.Courier)
        result: Result = await self._session.execute(stmt)
        db_couriers = result.scalars().all()

        if not db_couriers:
            return None

        couriers = [
            CourierResponse(
                id=courier.id,
                name=courier.name,
                location=Location(x=courier.location_x, y=courier.location_y),
                transport_id=courier.transport_id
            )
            for courier in db_couriers
        ]

        return GetAllCouriersResponse(couriers=couriers)