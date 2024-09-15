from datetime import datetime

from sqlalchemy import Column, Integer, String, JSON, DateTime

from app.db.session import Base


class Message(Base):
    __tablename__ = "messages"
    __table_args__ = {'comment': 'Table to store chat messages'}

    id = Column(Integer, primary_key=True, index=True)
    role = Column(String, nullable=False)
    parts = Column(JSON, nullable=False)
    intent = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<Message {self.id}>"

    def __str__(self):
        return self.__repr__()