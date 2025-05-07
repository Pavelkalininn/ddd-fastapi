import random
from dataclasses import dataclass
from typing import Any, Generator
from functools import total_ordering

from delivery_other.general_errors import Error, GeneralErrors
from delivery_other.primitives import Result


@total_ordering
class Location:
    _random = random.Random()
    MAX_DISTANCE = 10
    MIN_DISTANCE = 1

    def __init__(self, x: int, y: int):
        self._x = x
        self._y = y

    @property
    def x(self) -> int:
        return self._x

    @property
    def y(self) -> int:
        return self._y

    @staticmethod
    def create(x: int, y: int) -> Result['Location', Error]:
        if x < Location.MIN_DISTANCE or x > Location.MAX_DISTANCE:
            return Result.failure(GeneralErrors.value_is_invalid("x"))
        if y < Location.MIN_DISTANCE or y > Location.MAX_DISTANCE:
            return Result.failure(GeneralErrors.value_is_invalid("y"))
        return Result.success(Location(x, y))

    @staticmethod
    def create_random() -> 'Location':
        return Location(
            Location._random.randint(Location.MIN_DISTANCE,
                                     Location.MAX_DISTANCE),
            Location._random.randint(Location.MIN_DISTANCE,
                                     Location.MAX_DISTANCE)
        )

    def calculate_distance_to(self, other: 'Location') -> int:
        if other is None:
            raise ValueError("Other location cannot be None")

        x_distance = max(self.x, other.x) - min(self.x, other.x)
        y_distance = max(self.y, other.y) - min(self.y, other.y)

        return x_distance + y_distance

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Location):
            return False
        return self.x == other.x and self.y == other.y

    def __lt__(self, other: Any) -> bool:
        if not isinstance(other, Location):
            return NotImplemented
        return (self.x, self.y) < (other.x, other.y)

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __repr__(self) -> str:
        return f"Location(x={self.x}, y={self.y})"

    # Для совместимости с C# стилем
    @staticmethod
    def Create(x: int, y: int) -> Result['Location', Error]:
        return Location.create(x, y)

    @staticmethod
    def CreateRandom() -> 'Location':
        return Location.create_random()

    def CalculateDistanceTo(self, other: 'Location') -> int:
        return self.calculate_distance_to(other)