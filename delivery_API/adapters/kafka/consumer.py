import json
import logging
from uuid import UUID
from confluent_kafka import Consumer, KafkaException
from typing import Optional
from fastapi import Depends
from .schemas import BasketConfirmedIntegrationEvent
from .dependencies import get_mediator
from .commands import CreateOrderCommand


class KafkaConsumerService:
    def __init__(self, config: dict, topic: str):
        self._consumer = Consumer(config)
        self._topic = topic
        self._logger = logging.getLogger(__name__)

    async def consume_async(self):
        self._consumer.subscribe([self._topic])

        try:
            while True:
                msg = self._consumer.poll(1.0)

                if msg is None:
                    continue
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        self._logger.debug("Reached end of partition")
                    else:
                        self._logger.error(f"Consumer error: {msg.error()}")
                    continue

                try:
                    self._logger.info(
                        f"Received message at {msg.topic()}[{msg.partition()}]@{msg.offset()}")
                    event = self._parse_message(msg.value())

                    if event:
                        mediator = await get_mediator()
                        command = CreateOrderCommand(
                            basket_id=event.basket_id,
                            street=event.address.street
                        )
                        response = await mediator.send(command)

                        if response.is_err():
                            self._logger.error(
                                f"Failed to process order: {response.unwrap_err()}")
                        else:
                            self._consumer.store_offsets(msg)

                except json.JSONDecodeError as e:
                    self._logger.error(f"Failed to parse message: {e}")
                except Exception as e:
                    self._logger.error(f"Failed to process message: {e}")
                    # Можно добавить dead letter queue логику здесь

        except KeyboardInterrupt:
            pass
        finally:
            self._consumer.close()

    def _parse_message(self, message_value: str) -> Optional[
        BasketConfirmedIntegrationEvent]:
        try:
            data = json.loads(message_value)
            return BasketConfirmedIntegrationEvent(
                basket_id=UUID(data['basket_id']),
                address=Address(street=data['address']['street'])
            )
        except (KeyError, ValueError, TypeError) as e:
            self._logger.error(f"Invalid message format: {e}")
            return None