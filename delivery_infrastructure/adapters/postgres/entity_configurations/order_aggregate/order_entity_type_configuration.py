from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base

from delivery_core.domain.model.order_aggregate.order import Order
from delivery_core.domain.model.order_aggregate.order_status import OrderStatus
from delivery_core.domain.shared_kernel.location import Location

Base = declarative_base()


class OrderModel(Base):
    """SQLAlchemy model for Order entity"""

    __tablename__ = 'orders'

    id = Column(String(36), primary_key=True)  # UUID as string
    courier_id = Column(String(36), ForeignKey('couriers.id'), nullable=True)

    # Status as string enum
    status = Column(String(50), nullable=False)

    # Location as embedded values
    location_x = Column(Integer, nullable=False)
    location_y = Column(Integer, nullable=False)

    def to_domain(self) -> 'Order':
        """Convert to domain entity"""
        return Order(
            id=self.id,
            courier_id=self.courier_id,
            status=OrderStatus(self.status),
            location=Location(
                x=self.location_x,
                y=self.location_y
            )
        )

    @classmethod
    def from_domain(cls, order: 'Order') -> 'OrderModel':
        """Create from domain entity"""
        return cls(
            id=order.id,
            courier_id=order.courier_id,
            status=order.status.name,
            location_x=order.location.x,
            location_y=order.location.y
        )