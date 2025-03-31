from pydantic import BaseModel

class FileOut(BaseModel):
    filename: str
    filepath: str