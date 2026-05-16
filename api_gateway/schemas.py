from pydantic import BaseModel, EmailStr


class NotificationRequest(BaseModel):
    user_id: int
    email: EmailStr
    message: str