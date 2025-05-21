from dataclasses import dataclass
from uuid import UUID


@dataclass
class CreateOrderCommand:
    """Команда создания заказа

    Args:
        basket_id: Идентификатор корзины (совпадает с id заказа)
        street: Улица для доставки

    Raises:
        ValueError: При невалидных параметрах
    """
    basket_id: UUID
    street: str

    def __post_init__(self):
        """Валидация параметров"""
        if self.basket_id == UUID(int=0):
            raise ValueError("basket_id не может быть пустым")
        if not self.street or not self.street.strip():
            raise ValueError("street не может быть пустой строкой")