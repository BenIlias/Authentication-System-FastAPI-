from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)
    token = relationship('Token_list', back_populates='user', uselist=False)



class Token_list(Base):
    __tablename__ = 'tokenlist'

    id = Column(Integer, primary_key=True, nullable=False)
    refresh_token = Column(String, nullable=True)
    access_token = Column(String, nullable=True)
    revoked = Column(Boolean, default=False)
    user = relationship('User', back_populates='token')
    user_id = Column(Integer, ForeignKey('users.id'))
    