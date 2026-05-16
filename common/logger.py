import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

# Reduce kafka internal logs
logging.getLogger("kafka").setLevel(logging.WARNING)

logger = logging.getLogger("notification-service")