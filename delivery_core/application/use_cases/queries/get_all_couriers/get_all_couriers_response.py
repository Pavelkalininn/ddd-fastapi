from typing import List
from pydantic import BaseModel
from uuid import UUID

class Location(BaseModel):
    """Модель локации"""
    x: int  # Горизонталь
    y: int  # Вертикаль

class CourierResponse(BaseModel):
    """Модель ответа для курьера"""
    id: UUID
    name: str
    location: Location
    transport_id: UUID

class GetAllCouriersResponse(BaseModel):
    """Ответ на запрос всех курьеров"""
    couriers: List[CourierResponse] = []