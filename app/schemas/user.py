from pydantic import BaseModel, ConfigDict

class UserUpdate(BaseModel):
    username: str | None = None

class UserOut(BaseModel):
    id: int
    yandex_id: str
    username: str

    model_config = ConfigDict(from_attributes=True)  
