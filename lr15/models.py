import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime, UUID

from database import Base


class Message(Base):
    __tablename__ = "messages"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    username = Column(String)
    message = Column(String)
    send_datetime = Column(DateTime, default=datetime.now)
