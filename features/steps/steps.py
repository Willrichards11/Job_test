import os
import sys
import unittest

from behave import given, step, then, when
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import app
from database import TEST_DATABASE, Base, engine, get_db


engine = create_engine(
    TEST_DATABASE,
    connect_args={"check_same_thread": False}
    )
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
    )

# ensure all data is completly reset
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)


def override_get_db():
    ''' used to override main db for testing'''
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


# override db to use test database
app.dependency_overrides[get_db] = override_get_db
test_app = TestClient(app)
user_id = 132321


@given("the user id isnt taken")
def step_impl(context):
    """
    Asserts that the user id doesn't exist
    """
    response = test_app.get(f"/get_user_account/{user_id}")
    assert response.json() == []


@step("the user has added a user and account")
def step_impl(context):
    """
    Asserts that the user has created an account and user
    """
    id_added = test_app.post(f"/create_user/{user_id}")
    account_added = test_app.post(f"/create_account/{user_id}")
    assert id_added.status_code == 200, "Wrong status code"
    assert account_added.status_code == 200, "Wrong status code"


@then("the id should be placed in the users table with balance 100")
def step_impl(context):
    """
    Asserts that the new account should be present in the database
    """
    response = test_app.get(f"/get_user_account/{user_id}").json()
    assert response != []
    assert response[0]["userid"] == user_id
    assert response[0]["balance"] == 100
