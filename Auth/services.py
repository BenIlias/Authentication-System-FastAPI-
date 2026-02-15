from Auth.repository import AuthRepository
from Auth.schemas import LoginUser, RegisterUser
from fastapi import HTTPException, status
from passlib.context import CryptContext
from Auth.models import User
from utilities import token_generator, verify_token

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

        access_token = token_generator({'username': user_db.username})
        
        return {'access_token': access_token, 'token_type': 'Bearer'}


    def get_profile(self, token: str):
        return verify_token(token)
