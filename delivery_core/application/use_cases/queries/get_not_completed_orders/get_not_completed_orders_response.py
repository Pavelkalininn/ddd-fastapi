from typing import List
from pydantic import BaseModel
from uuid import UUID

class LocationResponse(BaseModel):
    """Модель локации для ответа"""
    x: int  # Горизонталь
    y: int  # Вертикаль

class OrderResponse(BaseModel):
    """Модель заказа для ответа"""
    id: UUID
    location: LocationResponse
    status: str  # 'created', 'assigned'

class GetNotCompletedOrdersResponse(BaseModel):
    """Ответ с незавершенными заказами"""
    orders: List[OrderResponse] = []