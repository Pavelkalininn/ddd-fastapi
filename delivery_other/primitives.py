from typing import Generic, TypeVar, Optional

T = TypeVar('T')
E = TypeVar('E', bound='Error')

class UnitResult(Generic[E]):
    @staticmethod
    def success() -> 'UnitResult[E]':
        return UnitResult[E]()

    @staticmethod
    def failure(error: E) -> 'UnitResult[E]':
        return UnitResult[E](error)

    def __init__(self, error: Optional[E] = None):
        self.error = error
        self.is_success = error is None

class Result(Generic[T, E]):
    @staticmethod
    def success(value: T) -> 'Result[T, E]':
        return Result[T, E](value=value)

    @staticmethod
    def failure(error: E) -> 'Result[T, E]':
        return Result[T, E](error=error)

    def __init__(self, value: Optional[T] = None, error: Optional[E] = None):
        self.value = value
        self.error = error
        self.is_success = error is None

