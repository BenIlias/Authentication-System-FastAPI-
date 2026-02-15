from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError

from fastapi import HTTPException


KEY = 'MYTOKENKEY'

def token_generator(data: dict, exp=5):
    
    data['exp'] = datetime.now(timezone.utc) + timedelta(minutes=exp)
    access_token = jwt.encode(data, KEY, algorithm="HS256")
    return access_token


def verify_token(token: str):
    try:
        payload = jwt.decode(token, KEY, algorithms=["HS256"])
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    return payload['username']


