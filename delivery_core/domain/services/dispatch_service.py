from delivery_core.domain.model.courier_aggregate.courier import Courier
from delivery_core.domain.model.courier_aggregate.courier_status import \
    CourierStatus
from delivery_core.domain.model.order_aggregate.order import Order
from delivery_other.general_errors import Error, GeneralErrors
from delivery_other.primitives import UnitResult


class DispatchService:
    def dispatch(self, order: Order) -> UnitResult[Error]:
        """
        Assigns the nearest available courier to an order

        Args:
            order: The order to be dispatched

        Returns:
            UnitResult[Error]: Success if dispatched, Error if failed
        """
        if not order:
            return UnitResult.failure(GeneralErrors.value_is_required("order"))

        # Get all free couriers
        free_couriers = [c for c in Courier.get_all() if
                         c.status == CourierStatus.free()]

        if not free_couriers:
            return UnitResult.failure(
                GeneralErrors.value_is_required("No available couriers"))

        # Find nearest courier
        nearest_courier = None
        min_steps = float('inf')

        for courier in free_couriers:
            steps = courier.get_steps_to_location(order.location)
            if steps < min_steps:
                min_steps = steps
                nearest_courier = courier

        # Assign order and courier to each other
        assign_result = nearest_courier.assign(order)
        if not assign_result.is_success:
            return assign_result

        order_assign_result = order.assign(nearest_courier)
        if not order_assign_result.is_success:
            return order_assign_result

        # Move courier to order location
        move_result = nearest_courier.move_to(order.location)
        return move_result