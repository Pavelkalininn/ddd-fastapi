import uuid

import pytest

from delivery_core.domain.model.courier_aggregate.courier import Courier
from delivery_core.domain.model.courier_aggregate.transport import Transport
from delivery_core.domain.shared_kernel.location import Location


@pytest.fixture
def create_courier():
    guid = uuid.uuid4()
    name = "Petya"
    transport = Transport.create("Good car", 1).value
    location = Location.create(1, 2).value

    return Courier.create(guid, name, transport, location)