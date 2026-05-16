import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from kafka.producer import KafkaProducer
from kafka.consumer import KafkaConsumer

from prometheus_client import start_http_server

from common.logger import logger

from common.metrics import (
    successful_notifications,
    failed_notifications,
    retried_notifications,
    dlq_notifications
)

import json
import time
import random


MAX_RETRIES = 3

TOPIC_NAME = "notifications"
DLQ_TOPIC = "notifications-dlq"


consumer = KafkaConsumer(
    TOPIC_NAME,
    bootstrap_servers='kafka:9092',
    auto_offset_reset='earliest',
    group_id='email-group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)


producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)


# Start Prometheus Metrics Server
start_http_server(8001)


print("Email Worker Started... Listening for messages")


for message in consumer:

    notification = message.value

    retry_count = notification.get("retry_count", 0)

    print("\nNew Notification Received")
    print(f"User ID: {notification['user_id']}")
    print(f"Email: {notification['email']}")
    print(f"Message: {notification['message']}")
    print(f"Retry Count: {retry_count}")

    time.sleep(2)

    success = random.choice([True, False])

    if success:

        logger.info("Email sent successfully")

        successful_notifications.inc()

    else:

        logger.error("Email sending failed")

        failed_notifications.inc()

        if retry_count < MAX_RETRIES:

            retry_count += 1

            logger.warning(
                f"Retrying notification... Attempt {retry_count}"
            )

            retried_notifications.inc()

            retry_notification = {
                "user_id": notification["user_id"],
                "email": notification["email"],
                "message": notification["message"],
                "retry_count": retry_count
            }

            producer.send(
                TOPIC_NAME,
                value=retry_notification
            )

            producer.flush()

        else:

            logger.critical(
                "Max retries exceeded. Sending to DLQ."
            )

            producer.send(
                DLQ_TOPIC,
                value=notification
            )

            producer.flush()

            logger.critical(
                "Notification sent to Dead Letter Queue"
            )

            dlq_notifications.inc()