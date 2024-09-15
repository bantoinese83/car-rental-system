from datetime import datetime
from pydantic import BaseModel, Field


class Message(BaseModel):
    role: str = Field(default="customer", description="The role of the message sender.")
    parts: dict = Field(default_factory=dict, description="The parts of the message content.")
    intent: str = Field(default="", description="The intent of the message.")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="The timestamp of the message.")