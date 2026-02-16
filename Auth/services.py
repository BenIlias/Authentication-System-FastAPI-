from Auth.repository import AuthRepository
from Auth.schemas import LoginUser, RegisterUser, Token_type
from fastapi import HTTPException, status
from passlib.context import CryptContext
from Auth.models import User, Token_list
from utilities import token_generate, verify_token

pwd_context = CryptContext(schemes=["bcrypt"])

class AuthService():
    def __init__(self, repository: AuthRepository):
        self.repository = repository
    
    def register_new_user(self, user_data: RegisterUser):
       
        if self.repository.get_user_by_username(user_data.username):
            raise HTTPException(status_code=409, detail="This user is already exists")

        if self.repository.get_user_by_email(user_data.email):
            raise HTTPException(status_code=409, detail="This user is already exists")

        
        user_dict = user_data.model_dump()
        hashed_password = pwd_context.hash(user_dict['password'])
        del user_dict['password']
        user_dict['hashed_password'] = hashed_password

        user_db = User(**user_dict)

        return self.repository.add_new_user(user_db)
        
    def login(self, user_data: LoginUser):
        user_db = self.repository.get_user_by_email(user_data.email)
        
        if not user_db:
            raise HTTPException(status_code=401, detail="Invalid email or password")

        if not pwd_context.verify(user_data.password, user_db.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid email or password")

        access_token = token_generate(Token_type.access_token.value, {'sub': user_db.username}, 1)
        refresh_token = token_generate(Token_type.refresh_token.value, {'sub': user_db.username}, 5)
        refresh_token_db = Token_list(user=user_db, refresh_token=refresh_token)
        self.repository.add_token(refresh_token_db)
        return {'access_token': access_token, 'refresh_token': refresh_token}


    def get_profile(self, token: str):
        username = verify_token(Token_type.access_token.value, token)
        return {'Message': f'Welcome {username}'}


    def get_refresh_token(self, refresh_token: str):
        return verify_token(Token_type.refresh_token.value, refresh_token)

    
    
