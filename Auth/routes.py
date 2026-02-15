from fastapi import APIRouter, Depends, Header, HTTPException
from database import get_db
from Auth.repository import AuthRepository
from Auth.services import AuthService
from sqlalchemy.orm import Session
from Auth.schemas import LoginUser, RegisterUser, UserOut, Token

router = APIRouter()



@router.post('/register', response_model=UserOut)
def login(userdata: RegisterUser, db: Session = Depends(get_db)):
    repository = AuthRepository(db)
    service = AuthService(repository)
    return service.register_new_user(userdata)
    


@router.post('/login', response_model=Token)
def login(userdata: LoginUser, db: Session = Depends(get_db)):
    repository = AuthRepository(db)
    service = AuthService(repository)
    return service.login(userdata)


@router.get('/profile')
def get_profile(Authorization: str | None = Header(default=None), db: Session = Depends(get_db)):
    if not Authorization or not Authorization.startswith('Bearer'):
                raise HTTPException(status_code=401, detail="Authorization header is required")

    
    token = Authorization.replace('Bearer ', '')
    repository = AuthRepository(db)
    service = AuthService(repository)
    return service.get_profile(token)