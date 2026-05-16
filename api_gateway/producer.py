from kafka.producer import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers='kafka:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

TOPIC_NAME = "notifications"


def send_notification(data):
    producer.send(TOPIC_NAME, value=data)
    producer.flush()