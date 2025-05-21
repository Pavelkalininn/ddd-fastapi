from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.ext.declarative import declarative_base

from delivery_core.domain.model.courier_aggregate.courier import Courier
from delivery_core.domain.model.courier_aggregate.courier_status import \
    CourierStatus
from delivery_core.domain.model.courier_aggregate.transport import Transport
from delivery_core.domain.shared_kernel.location import Location

Base = declarative_base()


class CourierModel(Base):
    """SQLAlchemy model for Courier entity"""

    __tablename__ = 'couriers'

    id = Column(String(36), primary_key=True)  # UUID as string
    name = Column(String(255), nullable=False)
    status = Column(String(50), nullable=False)  # Stored as string

    # Foreign key relationship to Transport
    transport_id = Column(String(36), ForeignKey('transports.id'),
                          nullable=False)
    transport = relationship("TransportModel")

    # Embedded Location value object
    location_x = Column(Integer, nullable=False)
    location_y = Column(Integer, nullable=False)

    def to_domain(self) -> 'Courier':
        """Convert to domain entity"""
        return Courier(
            id=self.id,
            name=self.name,
            status=CourierStatus(self.status),
            transport=Transport(
                id=self.transport.id,
                name=self.transport.name,
                speed=self.transport.speed
            ),
            location=Location(
                x=self.location_x,
                y=self.location_y
            )
        )

    @classmethod
    def from_domain(cls, courier: 'Courier') -> 'CourierModel':
        """Create from domain entity"""
        return cls(
            id=courier.id,
            name=courier.name,
            status=courier.status.name,
            transport_id=courier.transport.id,
            location_x=courier.location.x,
            location_y=courier.location.y
        )
