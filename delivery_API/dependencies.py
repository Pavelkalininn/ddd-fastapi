from .adapters.kafka.consumer import KafkaConsumerService

from .config import settings

def get_kafka_consumer() -> KafkaConsumerService:
    consumer_config = {
        'bootstrap.servers': settings.KAFKA_BOOTSTRAP_SERVERS,
        'group.id': 'DeliveryConsumerGroup',
        'auto.offset.reset': 'earliest',
        'enable.auto.commit': True,
        'enable.auto.offset.store': False,
        'enable.partition.eof': True
    }
    return KafkaConsumerService(
        config=consumer_config,
        topic=settings.BASKET_CONFIRMED_TOPIC
    )