from typing import List, Optional
import uuid
from sqlalchemy.orm import Session

from delivery_core.domain.model.courier_aggregate.courier import Courier
from delivery_core.domain.model.courier_aggregate.courier_status import \
    CourierStatus
from delivery_core.ports.i_courier_repository import ICourierRepository
from delivery_infrastructure.adapters.postgres.entity_configurations.courier_aggregate.courier_entity_type_configuration import \
    CourierModel
from delivery_infrastructure.adapters.postgres.entity_configurations.courier_aggregate.transport_entity_type_configuration import \
    TransportModel


class CourierRepository(ICourierRepository):
    def __init__(self, session: Session):
        self._session = session

    async def add_async(self, courier: Courier) -> Courier:
        courier_model = CourierModel.from_domain(courier)
        self._session.add(courier_model)
        return courier

    def update(self, courier: Courier) -> None:
        courier_model = CourierModel.from_domain(courier)
        self._session.merge(courier_model)

    async def get_async(self, courier_id: uuid.UUID) -> Optional[Courier]:
        courier_model = (
            self._session.query(CourierModel)
            .join(TransportModel)
            .filter(CourierModel.id == str(courier_id))
            .first()
        )

        if courier_model:
            return courier_model.to_domain()
        return None

    def get_all_in_free_status(self) -> List[Courier]:
        courier_models = (
            self._session.query(CourierModel)
            .join(TransportModel)
            .filter(CourierModel.status == CourierStatus.free().name)
            .all()
        )
        return [cm.to_domain() for cm in courier_models]