import uuid

import pytest

from delivery_core.domain.model.courier_aggregate.courier import Courier
from delivery_core.domain.model.courier_aggregate.courier_status import \
    CourierStatus
from delivery_core.domain.model.courier_aggregate.transport import Transport
from delivery_core.domain.model.order_aggregate.order import Order
from delivery_core.domain.services.dispatch_service import DispatchService
from delivery_core.domain.shared_kernel.location import Location


class TestDispatchService:
    @pytest.fixture
    def setup_couriers(self, monkeypatch):
        # Setup test couriers
        self.nearest_free = Courier(
            courier_id=uuid.uuid4(),
            location=Location(9, 9),
            transport=Transport(name='ffd', speed=3),
            name='s'
        )
        self.far_free = Courier(
            courier_id=uuid.uuid4(),
            location=Location(5, 5),
            transport=Transport(name='ffd', speed=3),
            name='s'
        )
        self.busy = Courier(
            courier_id=uuid.uuid4(),
            location=Location(10, 9),
            status=CourierStatus.busy(),
            transport=Transport(name='ffd', speed=3),
            name='s'
        )

        # Mock Courier.get_all()
        monkeypatch.setattr(
            Courier,
            'get_all',
            lambda: [self.nearest_free, self.far_free, self.busy]
        )

    def test_select_nearest_free_courier(self, setup_couriers):
        order_location = Location(10, 10)
        order = Order(location=order_location)

        service = DispatchService()
        result = service.dispatch(order)

        assert result.is_success
        assert order.courier_id == self.nearest_free.id
        assert self.nearest_free.location == order_location

    def test_return_error_when_no_free_couriers(self, monkeypatch):
        # Setup only busy couriers
        monkeypatch.setattr(
            Courier,
            'get_all',
            lambda: [
                Courier(status=CourierStatus.busy()),
                Courier(status=CourierStatus.busy())
            ]
        )

        order = Order(location=Location(0, 0))
        service = DispatchService()
        result = service.dispatch(order)

        assert not result.is_success
        assert "No available couriers" in result.error.message

    def test_return_error_when_order_is_none(self):
        service = DispatchService()
        result = service.dispatch(None)

        assert not result.is_success
        assert "Value order is required" in result.error.message