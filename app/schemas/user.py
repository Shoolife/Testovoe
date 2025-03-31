from pydantic import BaseModel

class UserCreate(BaseModel):
    yandex_id: str
    username: str

class UserOut(BaseModel):
    id: int
    yandex_id: str
    username: str

    class Config:
        orm_mode = True