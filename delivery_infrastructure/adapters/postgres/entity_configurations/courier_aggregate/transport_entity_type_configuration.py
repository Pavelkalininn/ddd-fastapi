from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

from delivery_core.domain.model.courier_aggregate.transport import Transport

Base = declarative_base()


class TransportModel(Base):
    """SQLAlchemy model for Transport entity"""

    __tablename__ = 'transports'

    id = Column(String(36), primary_key=True)  # UUID stored as string
    name = Column(String(255), nullable=False)
    speed = Column(Integer, nullable=False)

    def to_domain(self) -> 'Transport':
        """Convert to domain entity"""
        return Transport(
            id=self.id,
            name=self.name,
            speed=self.speed
        )

    @classmethod
    def from_domain(cls, transport: 'Transport') -> 'TransportModel':
        """Create from domain entity"""
        return cls(
            id=transport.id,
            name=transport.name,
            speed=transport.speed
        )