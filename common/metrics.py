from prometheus_client import Counter

successful_notifications = Counter(
    "successful_notifications_total",
    "Total successful notifications"
)

failed_notifications = Counter(
    "failed_notifications_total",
    "Total failed notifications"
)

retried_notifications = Counter(
    "retried_notifications_total",
    "Total retried notifications"
)

dlq_notifications = Counter(
    "dlq_notifications_total",
    "Total notifications sent to DLQ"
)