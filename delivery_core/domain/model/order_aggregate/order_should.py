import uuid
import pytest
from delivery_core.domain.model.order_aggregate.order import Order
from delivery_core.domain.model.order_aggregate.order_status import \
    OrderStatus
from delivery_core.domain.shared_kernel.location import Location


class TestOrder:
    @staticmethod
    def get_invalid_order_data():
        return [
            (None, Location.create(1, 2).value),
            (uuid.uuid4(), None)
        ]

    @pytest.mark.parametrize("order_id,location", get_invalid_order_data())
    def test_return_error_when_params_incorrect(self, order_id, location):
        order_result = Order.create(order_id, location)
        assert not order_result.is_success
        assert order_result.error is not None

    def test_be_correct_when_params_correct(self):
        guid = uuid.uuid4()
        location = Location.create(1, 2).value

        order_result = Order.create(guid, location)
        assert order_result.is_success
        assert order_result.value.id == guid
        assert order_result.value.location == location
        assert order_result.value.status == OrderStatus.created()

    def test_can_assign_when_created_and_cannot_when_assigned(self):
        order = Order.create(uuid.uuid4(), Location.create(1, 2).value).value

        assign_result = order.assign()
        assert assign_result.is_success
        assert order.status == OrderStatus.assigned()

        second_assign = order.assign()
        assert not second_assign.is_success
        assert second_assign.error is not None

    def test_can_complete_when_assigned(self):
        order = Order.create(uuid.uuid4(), Location.create(1, 2).value).value
        order.assign()

        complete_result = order.complete()
        assert complete_result.is_success
        assert order.status == OrderStatus.completed()

        second_complete = order.complete()
        assert not second_complete.is_success
        assert second_complete.error is not None