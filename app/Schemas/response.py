from pydantic import BaseModel


class Response(BaseModel):
    message: str

    class Config:
        orm_mode = True

