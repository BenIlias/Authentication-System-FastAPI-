from sqlalchemy.orm import Session
from Auth.models import User

class AuthRepository():
    def __init__(self, db: Session):
        self.db = db
    
    
    def get_user_by_email(self, email):
        return self.db.query(User).filter(User.email == email ).first()

    def get_user_by_username(self, username):
        return self.db.query(User).filter(User.username == username).first()


    def add_new_user(self, userData):
        self.db.add(userData)
        self.db.commit()
        self.db.refresh(userData)
        return userData

    