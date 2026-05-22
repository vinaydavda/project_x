import os
import time
import logging
import pika
import json
from dotenv import load_dotenv

connection = None
channel = None
load_dotenv()

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")

_logger = logging.getLogger(__name__)

def connect_rabbitmq():
    global connection, channel

    while True:
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(RABBITMQ_HOST, heartbeat=600, blocked_connection_timeout=300)
            )

            channel = connection.channel()

            channel.queue_declare(queue="product_events", durable=True)
            _logger.info(f"[RabbitMQ Connection] - Connected to rabbitmq")
            break
        except Exception as e:
            _logger.error(f"[RabbitMQ Connection] - Rabbitmq connection issue, retrying...: {e}")
            time.sleep(5)



def get_channel():
    return channel


def close_rabbitmq():
    global connection

    if connection and connection.is_open:
        connection.close()

def publish_event(event_type, event_data):
    try:
        channel.basic_publish(
            exchange="",
            routing_key=event_type,
            body=json.dumps(event_data),
            properties=pika.BasicProperties(
                delivery_mode=2
            )
        )
        _logger.info(f"[RabbitMQ] - Event Published: {event_data}")
    except Exception as e:
        _logger.error(f"[RabbitMQ] - Error publishing event: {event_data}: {e}")
