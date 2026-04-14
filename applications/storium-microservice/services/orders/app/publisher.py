import json
import logging
from typing import Any

import pika

from app.config import get_settings

logger = logging.getLogger(__name__)


def publish_order_created(payload: dict[str, Any]) -> None:
    s = get_settings()
    if not s.rabbitmq_url:
        logger.warning("RABBITMQ_URL tanımlı değil; sipariş olayı yayınlanmadı")
        return
    try:
        params = pika.URLParameters(s.rabbitmq_url)
        conn = pika.BlockingConnection(params)
        ch = conn.channel()
        ch.exchange_declare(exchange=s.rabbitmq_exchange, exchange_type="topic", durable=True)
        body = json.dumps(payload, default=str).encode("utf-8")
        ch.basic_publish(
            exchange=s.rabbitmq_exchange,
            routing_key=s.rabbitmq_routing_key,
            body=body,
            properties=pika.BasicProperties(
                content_type="application/json",
                delivery_mode=2,
            ),
        )
        conn.close()
    except Exception:
        logger.exception("RabbitMQ publish failed; order already persisted")
