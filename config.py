from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    GEO_SERVICE_GRPC_HOST: str
    KAFKA_BOOTSTRAP_SERVERS: str
    BASKET_CONFIRMED_TOPIC: str = "basket_confirmed"

    class Config:
        env_file = ".env"


settings = Settings()
