import uuid
from typing import List, Tuple

import pytest

from delivery_core.domain.model.courier_aggregate.courier import Courier
from delivery_core.domain.model.courier_aggregate.courier_status import \
    CourierStatus
from delivery_core.domain.model.courier_aggregate.transport import Transport
from delivery_core.domain.model.order_aggregate.order import Order
from delivery_core.domain.shared_kernel.location import Location


class TestCourier:
    @staticmethod
    def get_invalid_courier_data() -> List[Tuple]:
        return [
            (None, "Petya", Transport.create("Good car", 1),
             Location.create(1, 2)),
            (uuid.uuid4(), None, Transport.create("Good car", 1),
             Location.create(1, 2)),
            (uuid.uuid4(), "Petya", None, Location.create(1, 2)),
            (uuid.uuid4(), "Petya", Transport.create("Good car", 1), None)
        ]

    @pytest.mark.parametrize("courier_id,name,transport,location",
                             get_invalid_courier_data())
    def test_return_error_when_params_incorrect(self, courier_id, name,
                                                transport, location):
        result = Courier.create(courier_id, name, transport, location)
        assert not result.is_success
        assert result.error is not None

    def test_be_correct_when_params_correct(self):
        guid = uuid.uuid4()
        name = "Petya"
        transport = Transport.create("Good car", 1)
        location = Location.create(1, 2)

        courier = Courier.create(guid, name, transport, location)
        assert courier.is_success
        assert courier.value.id == guid
        assert courier.value.name == name
        assert courier.value.transport == transport
        assert courier.value.location == location
        assert courier.value.status == CourierStatus.free

    def test_can_assign_when_free_and_cannot_when_busy(self):
        order_id = Order.create(
                uuid.uuid4(),
                Location.create(1, 2).value
            ).value.courier_id
        courier = Courier.create(uuid.uuid4(), "Petya",
                                 Transport.create("Good car", 1).value,
                                 Location.create(1, 2).value).value

        assign_result = courier.assign(order_id)
        assert assign_result.is_success
        assert courier.status == CourierStatus.busy

        second_assign = courier.assign(order_id)
        assert not second_assign.is_success
        assert second_assign.error is not None

    def test_can_complete_when_busy(self):
        courier = Courier.create(uuid.uuid4(), "Petya",
                                 Transport.create("Good car", 1).value,
                                 Location.create(1, 2).value).value
        courier.assign(Order.create(
                uuid.uuid4(),
                Location.create(1, 2).value
            ).value.courier_id)

        complete_result = courier.complete()
        assert complete_result.is_success
        assert courier.status == CourierStatus.free

        second_complete = courier.complete()
        assert not second_complete.is_success
        assert second_complete.error is not None

    def test_get_step_count_correct(self):
        destination = Location.create(5, 5)
        courier = Courier.create(uuid.uuid4(), "Petya",
                                 Transport.create("Bicycle", 1).value,
                                 Location.create(1, 1).value).value
        assert courier.get_step_count(
            destination.value).value == 8  # Manhattan distance (4+4)/1

    def test_move_correct(self):
        target = Location.create(5, 5).value
        courier = Courier.create(uuid.uuid4(), "Petya",
                                 Transport.create("Bicycle", 2).value,
                                 Location.create(1, 1).value).value
        courier.move(target)
        assert courier.location == Location.create(3, 1).value