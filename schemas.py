from pydantic import BaseModel


class User(BaseModel):
    '''Defines database schema and datatypes for the users table '''
    id: int

    class Config:
        orm_mode = True


class Account(BaseModel):
    '''Defines database schema and datatypes for the accounts table '''

    id: int
    userid: int
    balance: float

    class Config:
        orm_mode = True
