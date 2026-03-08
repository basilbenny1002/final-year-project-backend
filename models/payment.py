from pydantic import BaseModel

class NotificationPayload(BaseModel):
    title: str
    content: str
