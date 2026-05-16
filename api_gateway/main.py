import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi import FastAPI, HTTPException

from api_gateway.schemas import NotificationRequest
from producer import send_notification

from common.database import engine, SessionLocal
from common.models import Base, Notification
from common.redis_client import redis_client

from prometheus_client import generate_latest
from fastapi.responses import Response


app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.get("/")
def home():

    return {
        "message": "Notification Service Running"
    }
    
@app.get("/metrics")
def metrics():

    return Response(
        generate_latest(),
        media_type="text/plain"
    )


@app.post("/notify")
def notify_user(request: NotificationRequest):

    # Rate Limiting

    user_key = f"user:{request.user_id}"

    request_count = redis_client.get(user_key)

    if request_count and int(request_count) >= 5:

        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded. Try again later."
        )

    pipe = redis_client.pipeline()

    pipe.incr(user_key, 1)
    pipe.expire(user_key, 60)

    pipe.execute()

    # Database

    db = SessionLocal()

    notification = Notification(
        user_id=request.user_id,
        email=request.email,
        message=request.message
    )

    db.add(notification)
    db.commit()
    db.refresh(notification)

    # Kafka Event

    notification_data = {
        "notification_id": notification.id,
        "user_id": request.user_id,
        "email": request.email,
        "message": request.message
    }

    send_notification(notification_data)

    return {
        "status": "success",
        "message": "Notification queued successfully"
    }