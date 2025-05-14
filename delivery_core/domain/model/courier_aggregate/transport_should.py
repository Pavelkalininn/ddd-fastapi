import pytest
from uuid import UUID

from delivery_core.domain.model.courier_aggregate.transport import Transport


class TestTransport:
    @staticmethod
    def get_invalid_transport_data():
        return [
            ("Good car", 0),
            ("Good car", -1),
            (None, 3)
        ]

    @staticmethod
    def get_invalid_speeds():
        return [0, -1]

    def test_be_correct_when_params_is_correct_on_created(self):
        transport_name = "Delivery car"
        transport_speed = 3
        transport_result = Transport.create(transport_name, transport_speed)

        assert transport_result.is_success
        assert isinstance(transport_result.value.id, UUID)
        assert transport_result.value.name == transport_name
        assert transport_result.value.speed == transport_speed

    @pytest.mark.parametrize("name,speed", get_invalid_transport_data())
    def test_return_error_when_params_is_incorrect_on_created(self, name,
                                                              speed):
        transport_result = Transport.create(name, speed)

        assert not transport_result.is_success
        assert transport_result.error is not None
        if name is None:
            assert transport_result.error.code == "value.is.required"
        else:
            assert transport_result.error.code == "value.is.invalid"

    def test_can_set_speed_when_speed_is_correct(self):
        transport = Transport.create('Transport', 1).value
        transport.speed = 2
        assert transport.speed == 2

    @pytest.mark.parametrize("speed", get_invalid_speeds())
    def test_return_error_when_speed_is_incorrect(self, speed):
        transport = Transport.create('First car', 2).value
        try:
            transport.speed = speed
            pytest.fail("Expected ValueError to be raised")
        except ValueError as e:
            assert str(e) == "Speed must be between 1 and 3"