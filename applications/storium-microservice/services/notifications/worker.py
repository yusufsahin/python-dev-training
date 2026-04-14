import json
import logging
import os
import sys
import time

import pika

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)


def main() -> None:
    url = os.environ.get("RABBITMQ_URL", "amqp://storium:storium_pass@localhost:5672/")
    exchange = os.environ.get("RABBITMQ_EXCHANGE", "storium.events")
    queue = os.environ.get("NOTIFICATIONS_QUEUE", "storium.notifications")
    routing_key = os.environ.get("RABBITMQ_ORDER_ROUTING_KEY", "order.created")

    while True:
        try:
            params = pika.URLParameters(url)
            conn = pika.BlockingConnection(params)
            ch = conn.channel()
            ch.exchange_declare(exchange=exchange, exchange_type="topic", durable=True)
            ch.queue_declare(queue=queue, durable=True)
            ch.queue_bind(exchange=exchange, queue=queue, routing_key=routing_key)
            logger.info("Bound queue %s to %s with key %s", queue, exchange, routing_key)

            def on_message(
                _ch: pika.channel.Channel,
                method: pika.spec.Basic.Deliver,
                _props: pika.spec.BasicProperties,
                body: bytes,
            ) -> None:
                try:
                    payload = json.loads(body.decode("utf-8"))
                except json.JSONDecodeError:
                    logger.warning("Invalid JSON: %s", body[:200])
                else:
                    logger.info("Notification event: %s", payload)
                _ch.basic_ack(delivery_tag=method.delivery_tag)

            ch.basic_qos(prefetch_count=10)
            ch.basic_consume(queue=queue, on_message_callback=on_message)
            logger.info("Consuming from %s", queue)
            ch.start_consuming()
        except pika.exceptions.AMQPConnectionError as e:
            logger.warning("RabbitMQ not ready: %s; retry in 3s", e)
            time.sleep(3)
        except KeyboardInterrupt:
            logger.info("Stopping")
            sys.exit(0)


if __name__ == "__main__":
    main()
