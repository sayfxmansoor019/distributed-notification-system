from kafka.consumer import KafkaConsumer
import json

DLQ_TOPIC = "notifications-dlq"

consumer = KafkaConsumer(
    DLQ_TOPIC,
    bootstrap_servers='kafka:9092',
    auto_offset_reset='earliest',
    group_id='dlq-group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

print("DLQ Consumer Started...")

for message in consumer:

    notification = message.value

    print("\nFAILED NOTIFICATION RECEIVED IN DLQ")
    print(notification)