import uuid
from typing import Any

from delivery_core.domain.shared_kernel.location import Location
from delivery_other.general_errors import Error, GeneralErrors
from delivery_other.primitives import Result


class Transport:
    def __init__(self, name: str, speed: int):
        self._id = uuid.uuid4()
        self._name = name
        self._speed = speed

    @property
    def id(self) -> uuid.UUID:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def speed(self) -> int:
        return self._speed

    @speed.setter
    def speed(self, value: int) -> None:
        if value < 1 or value > 3:
            raise ValueError("Speed must be between 1 and 3")
        self._speed = value

    @staticmethod
    def create(name: str, speed: int) -> Result['Transport', Error]:
        if not name:
            return Result.failure(GeneralErrors.value_is_required("name"))
        if speed < 1 or speed > 3:
            return Result.failure(GeneralErrors.value_is_required("speed"))
        return Result.success(Transport(name, speed))

    def move(self, current: Location, target: Location) -> Result[Location, Error]:
        if not current:
            return Result.failure(GeneralErrors.value_is_required("current"))
        if not target:
            return Result.failure(GeneralErrors.value_is_required("target"))

        dif_x = target.x - current.x
        dif_y = target.y - current.y
        cruising_range = self._speed

        move_x = max(-cruising_range, min(dif_x, cruising_range))
        cruising_range -= abs(move_x)
        move_y = max(-cruising_range, min(dif_y, cruising_range))

        new_location = Location(current.x + move_x, current.y + move_y)
        return Result.success(new_location)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Transport):
            return False
        return self._id == other._id

    def __hash__(self) -> int:
        return hash(self._id)

    def __repr__(self) -> str:
        return f"Transport(id={self._id}, name='{self._name}', speed={self._speed})"