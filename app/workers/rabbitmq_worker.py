import os
import time
import json
import pika
import logging
from app.models.query_handler import create_product, update_product, delete_product
from dotenv import load_dotenv

load_dotenv()
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")

logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger(__name__)

while True:
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(RABBITMQ_HOST, heartbeat=600, blocked_connection_timeout=300)
        )
        _logger.info(f"[READ DB] - Connected to rabbitmq")
        break
    except Exception as e:
        _logger.error(f"[READ DB] - Rabbitmq connection issue, retrying...: {e}")
        time.sleep(5)

channel = connection.channel()

channel.queue_declare(queue="product_events", durable=True)
channel.basic_qos(prefetch_count=1)


def callback(ch, method, properties, body):
    # Sample data body:
    # body = {
    #     "event_id": "a6b25435-c1ae-4442-bbbc-9b155ed41cbc",
    #     "event_name": "product",
    #     "event_type": "PRODUCT_UPDATE",
    #     "event_sequence": 3,
    #     "event_data": {
    #         "name": "Apple",
    #         "price": 100
    #     }
    # }

    try:
        _logger.info(f">> Received... {body}")

        body = json.loads(body.decode())
        event_data = body["event_data"]
        event_data["id"] = body["event_id"]
        
        if body["event_type"] == "PRODUCT_CREATE":
            event_data["active"] = True
            create_product(event_data)
        
        elif body["event_type"] == "PRODUCT_UPDATE":
            event_data["active"] = True
            update_product(event_data["id"], event_data)
        
        elif body["event_type"] == "PRODUCT_DELETE":
            delete_product(event_data["id"])

        ch.basic_ack(delivery_tag=method.delivery_tag)

    except Exception as e:
        _logger.error(f"[READ DB] - Error while operating on Read DB: {e}")
        ch.basic_nack(
            delivery_tag=method.delivery_tag,
            requeue=True
        )

channel.basic_consume(
    queue="product_events",
    on_message_callback=callback,
    auto_ack=False
)

_logger.info(f"[READ DB] - Worker Started...")

channel.start_consuming()