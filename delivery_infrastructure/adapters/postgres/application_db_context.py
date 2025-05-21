from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
import os

from delivery_infrastructure.adapters.postgres.entity_configurations.courier_aggregate.courier_entity_type_configuration import \
    CourierModel
from delivery_infrastructure.adapters.postgres.entity_configurations.courier_aggregate.transport_entity_type_configuration import \
    TransportModel
from delivery_infrastructure.adapters.postgres.entity_configurations.order_aggregate.order_entity_type_configuration import \
    OrderModel

Base = declarative_base()

class Database:
    def __init__(self):
        self.engine = create_engine(os.getenv("DB_CREDS"))
        self.session_factory = sessionmaker(
            bind=self.engine,
            autocommit=False,
            autoflush=False
        )
        self.Session = scoped_session(self.session_factory)

    def init_models(self):
        """Initialize all database models"""
        CourierModel
        TransportModel
        OrderModel
        Base.metadata.create_all(bind=self.engine)

    def get_session(self):
        """Get a new database session"""
        return self.Session()

# Initialize database instance
db = Database()