from pathlib import Path

from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

import crud
import schemas
from database import engine, SessionLocal
from models import Base

BASE_DIR = Path(__file__).resolve().parent
app = FastAPI()
templates = Jinja2Templates(directory=BASE_DIR / "templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    Base.metadata.create_all(bind=engine)


@app.get("/chat", response_class=HTMLResponse)
async def chat(request: Request, db: Session = Depends(get_db)):
    messages = crud.get_messages(db, limit=100)
    return templates.TemplateResponse("chat.html", {"request": request, "messages": messages})


@app.post("/chat/messages", response_model=schemas.Message)
async def create_message(message: schemas.Message, db: Session = Depends(get_db)):
    return crud.create_message(db=db, message=message)


@app.get("/chat/messages", response_model=list[schemas.Message])
async def read_messages(db: Session = Depends(get_db)):
    return crud.get_messages(db=db)


if __name__ == "__main__":
    create_tables()
