from pydantic import BaseModel


class Message(BaseModel):
    username: str
    message: str

    class Config:
        from_attributes = True
