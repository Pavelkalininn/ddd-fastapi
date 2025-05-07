from functools import total_ordering


@total_ordering
class CourierStatus:
    def __init__(self, name: str):
        self._name = name.lower()

    @property
    def name(self) -> str:
        return self._name

    @staticmethod
    def free() -> 'CourierStatus':
        return CourierStatus("free")

    @staticmethod
    def busy() -> 'CourierStatus':
        return CourierStatus("busy")

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, CourierStatus):
            return False
        return self._name == other._name

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, CourierStatus):
            return NotImplemented
        return self._name < other._name

    def __hash__(self) -> int:
        return hash(self._name)

    def __repr__(self) -> str:
        return f"CourierStatus({self._name})"
