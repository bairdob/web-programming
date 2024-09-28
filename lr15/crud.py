from typing import Type

from sqlalchemy.orm import Session

import models
import schemas


def get_messages(db: Session, limit: int = 100) -> list[Type[models.Message]]:
    return db.query(models.Message).order_by(models.Message.send_datetime.asc()).limit(limit).all()


def create_message(db: Session, message: schemas.Message) -> models.Message:
    db_message = models.Message(**message.model_dump())
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message
