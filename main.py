from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import asynccontextmanager
import os
from typing import AsyncGenerator

from delivery_core.application.use_cases.queries.get_all_couriers.get_all_couriers_handler import \
    GetAllCouriersHandler
from delivery_core.application.use_cases.queries.get_all_couriers.get_all_couriers_query import \
    GetAllCouriersQuery
from delivery_core.application.use_cases.queries.get_all_couriers.get_all_couriers_response import \
    GetAllCouriersResponse
from delivery_core.application.use_cases.queries.get_not_completed_orders.get_not_completed_orders_handler import \
    GetNotCompletedOrdersHandler
from delivery_core.application.use_cases.queries.get_not_completed_orders.get_not_completed_orders_query import \
    GetNotCompletedOrdersQuery
from delivery_core.application.use_cases.queries.get_not_completed_orders.get_not_completed_orders_response import \
    GetNotCompletedOrdersResponse
from delivery_core.domain.services.dispatch_service import DispatchService

from delivery_infrastructure.adapters.postgres.entity_configurations.courier_aggregate.courier_entity_type_configuration import \
    CourierModel
from delivery_infrastructure.adapters.postgres.entity_configurations.courier_aggregate.transport_entity_type_configuration import \
    TransportModel
from delivery_infrastructure.adapters.postgres.entity_configurations.order_aggregate.order_entity_type_configuration import \
    OrderModel

from delivery_infrastructure.adapters.postgres.repositories.courier_repository import \
    CourierRepository
from delivery_infrastructure.adapters.postgres.repositories.order_repository import \
    OrderRepository
from delivery_infrastructure.adapters.postgres.unit_of_work import UnitOfWork

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    engine = create_engine(os.getenv("DB_CREDS"))
    OrderModel.metadata.create_all(bind=engine)
    TransportModel.metadata.create_all(bind=engine)
    CourierModel.metadata.create_all(bind=engine)
    yield
    # Cleanup on shutdown
    engine.dispose()

app = FastAPI(lifespan=lifespan)

# Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency Injection Setup
def get_db():
    engine = create_engine(os.getenv("CONNECTION_STRING"))
    local_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = local_session()
    try:
        yield db
    finally:
        db.close()

def get_dispatch_service() -> DispatchService:
    return DispatchService()

def get_unit_of_work(db = Depends(get_db)) -> UnitOfWork:
    return UnitOfWork(db)

def get_courier_repository(db = Depends(get_db)) -> CourierRepository:
    return CourierRepository(db)

def get_order_repository(db = Depends(get_db)) -> OrderRepository:
    return OrderRepository(db)

# Register dependencies
# app.dependency_overrides.update({
#     DispatchService: get_dispatch_service,
#     UnitOfWork: get_unit_of_work,
#     CourierRepository: get_courier_repository,
#     OrderRepository: get_order_repository
# })

# Health Check
@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.get("/couriers", response_model=GetAllCouriersResponse)
async def get_couriers(
    handler: GetAllCouriersHandler = Depends(GetAllCouriersHandler)
):
    response = await handler.handle(GetAllCouriersQuery())
    if not response:
        raise HTTPException(status_code=404, detail="No couriers found")
    return response

@app.get("/orders/not-completed", response_model=GetNotCompletedOrdersResponse)
async def get_not_completed_orders(
    handler: GetNotCompletedOrdersHandler = Depends(GetNotCompletedOrdersHandler)
):
    response = await handler.handle(GetNotCompletedOrdersQuery())
    if not response:
        raise HTTPException(status_code=404, detail="No active orders found")
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)