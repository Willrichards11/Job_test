from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    '''
    A simple users table with just a user_id. Joins to the accounts table with
    a one to many relationship
    '''
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    def __init__(self, id):
        self.id = id


class Account(Base):
    '''
    A simple Accounts table with user id (foreign key to users.id) and an
    account balance.
    '''
    __tablename__ = "Accounts"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    userid = Column(Integer)
    balance = Column(Float)

    def __init__(self, userid, balance):
        self.userid = userid
        self.balance = balance
