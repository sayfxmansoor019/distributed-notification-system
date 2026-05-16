from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from common.database import Base


class Notification(Base):

    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer)

    email = Column(String)

    message = Column(String)

    status = Column(String, default="PENDING")

    retry_count = Column(Integer, default=0)

    created_at = Column(DateTime, default=datetime.utcnow)