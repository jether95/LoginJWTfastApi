from typing import Optional
from pydantic import BaseModel


class UserBase(BaseModel):
    # id: Optional[int]
    user: str
    password: str

    class Config:
        orm_mode = True
