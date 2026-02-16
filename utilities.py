from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError, ExpiredSignatureError
from Auth.schemas import Token_type
from fastapi import HTTPException, status


ACCESS_TOKEN_KEY = 'MYACCESSTOKENKEY'
REFRESH_TOKEN_KEY = 'MYREFRESHTOKENKEY'


def token_generate(token_type: Token_type, data: dict, exp=1):

    key = ACCESS_TOKEN_KEY if token_type == Token_type.access_token else REFRESH_TOKEN_KEY

    data['exp'] = datetime.now(timezone.utc) + timedelta(minutes=exp)

    token = jwt.encode(data, key, algorithm="HS256")
    return token


def verify_token(token_type: Token_type, token: str):
    key = ACCESS_TOKEN_KEY if token_type == Token_type.access_token else REFRESH_TOKEN_KEY 
    try:
        payload = jwt.decode(token, key, algorithms=["HS256"])
        if token_type == Token_type.refresh_token:
            return token_generate(Token_type.access_token, {'sub': payload['sub']})
    
    except ExpiredSignatureError:
        if token_type == Token_type.access_token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={'Message': 'Access token is Expired'})
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail={'Message': 'Refresh Token Expired, you need to Loggin Again'})


        #payload = jwt.decode(token, key, algorithms=["HS256"], options={"verify_exp": False})

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    

    return payload['sub']


