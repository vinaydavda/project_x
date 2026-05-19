import logging
import pika
import json

connection = None
channel = None

_logger = logging.getLogger(__name__)

def connect_rabbitmq():
    global connection, channel

    connection = pika.BlockingConnection(
        pika.ConnectionParameters("localhost")
    )

    channel = connection.channel()

    channel.queue_declare(queue="product_events")


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
            body=json.dumps(event_data)
        )
        _logger.info(f"[RabbitMQ] - Event Published: {event_data}")
    except Exception as e:
        _logger.error(f"[RabbitMQ] - Error publishing event: {event_data}: {e}")
