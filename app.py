from typing import List

import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse

import models
import schemas
from database import SessionLocal, engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


def string_is_integer(string):
    '''test to see if account is convertible to int'''
    try:
        int(string)
        return True
    except ValueError:
        return False


@app.get("/get_user_account/{account_id}")
async def get_user_account(account_id, db: Session = Depends(get_db)):
    if not string_is_integer(account_id):
        return "not a valid integer"

    records = (
        db.query(models.Account)
        .filter(models.Account.userid == account_id)
        .all()
    )
    return records


@app.post("/create_user/{account_id}")
async def create_user(account_id, db: Session = Depends(get_db)):
    if not string_is_integer(account_id):
        return "not a valid integer"

    # if user if exists
    elif (
        db.query(models.User.id).filter(models.User.id == account_id).count()
        > 0
    ):
        return "User id already exists"

    user = models.User(int(account_id))
    db.add(user)
    db.commit()
    return f"User created with id {account_id}"


@app.post("/create_account/{account_id}")
async def create_account(account_id, db: Session = Depends(get_db)):
    if not string_is_integer(account_id):
        return "not a valid integer"

    account = models.Account(int(account_id), 100)
    db.add(account)
    db.commit()
    return f"account created with id {account_id}"


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
