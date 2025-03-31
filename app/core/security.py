from jose import jwt
from datetime import datetime, timedelta

def create_access_token(data: dict, secret: str, algorithm: str, expires_delta: int = 60):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_delta)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, secret, algorithm=algorithm)