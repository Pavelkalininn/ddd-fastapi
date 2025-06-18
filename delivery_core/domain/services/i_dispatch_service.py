from abc import ABC, abstractmethod

from delivery_core.domain.model.order_aggregate.order import Order
from delivery_other.general_errors import Error
from delivery_other.primitives import UnitResult



class AbstractDispatchService(ABC):
    """Abstract base class for dispatch services"""

    @abstractmethod
    def dispatch(self, order: Order) -> UnitResult[Error]:
        """
        Assign a courier to the specified order

        Args:
            order: The order to be dispatched

        Returns:
            UnitResult[Error]: Success if dispatched successfully,
                            Error if dispatch failed
        """
        pass