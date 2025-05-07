from typing import Any
from functools import total_ordering


@total_ordering
class OrderStatus:
    """
    Статус заказа
    """

    def __init__(self, name: str):
        """
        Конструктор

        :param name: Название статуса
        """
        self._name = name.lower()

    @property
    def name(self) -> str:
        """
        Название статуса
        """
        return self._name

    @staticmethod
    def created() -> 'OrderStatus':
        """Статус 'Создан'"""
        return OrderStatus("created")

    @staticmethod
    def assigned() -> 'OrderStatus':
        """Статус 'Назначен'"""
        return OrderStatus("assigned")

    @staticmethod
    def completed() -> 'OrderStatus':
        """Статус 'Завершен'"""
        return OrderStatus("completed")

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, OrderStatus):
            return False
        return self._name == other._name

    def __lt__(self, other: Any) -> bool:
        if not isinstance(other, OrderStatus):
            return NotImplemented
        return self._name < other._name

    def __hash__(self) -> int:
        return hash(self._name)

    def __repr__(self) -> str:
        return f"OrderStatus({self._name})"
