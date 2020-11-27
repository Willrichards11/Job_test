import os
import sys
import unittest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import app
from database import TEST_DATABASE, Base, engine, get_db

engine = create_engine(TEST_DATABASE, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)
Base.metadata.create_all(bind=engine)


def override_get_db():
    ''' used to override main db for testing'''

    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


class TestApi(unittest.TestCase):
    def setUp(self):
        '''
        Configures the testing environment for the test cases
        '''
        user_id = 1231231
        test_app = TestClient(app)
        self.engine = engine
        self.rspnse_acnt_bef = test_app.get(f"/get_user_account/{user_id}")
        self.rspnse_bef_no_id = test_app.get(f"/get_user_account")
        self.rspnse_crt_user = test_app.post(f"/create_user/{user_id}")
        self.rspnse_user_no_id = test_app.get(f"/create_user")
        self.rspnse_crt_account = test_app.post(f"/create_account/{user_id}")
        self.rspnse_account_no_id = test_app.get(f"/create_account")
        self.rspnse_acnt_bef_invalid = test_app.get(f"/get_user_account/s")
        self.rspnse_crt_user_invalid = test_app.post(f"/create_user/s")
        self.rspnse_crt_account_invalid = test_app.post(f"/create_account/s")


    def tearDown(self):
        '''
        Shuts down the testing environment by deleting all metadata from the
        testing database.
        '''
        Base.metadata.drop_all(self.engine)

    def test_endpoints(self):
        '''
        Basic unit tests for the endpoints defined in app.py,
        '''
        # make endpoint calls with a correct user id
        assert self.rspnse_acnt_bef.status_code == 200, "Wrong status code"
        assert self.rspnse_crt_user.status_code == 200, "Wrong status code"
        assert self.rspnse_crt_account.status_code == 200, "Wrong status code"

        # make endpoint calls with an incorrect user id
        assert self.rspnse_bef_no_id.status_code == 404, "Wrong status code"
        assert self.rspnse_user_no_id.status_code == 404, "Wrong status code"
        assert self.rspnse_account_no_id.status_code == 404, "Wrong status code"
        assert type(self.rspnse_acnt_bef.json()) == list

        # ensure non-integer ids are invalid
        assert self.rspnse_acnt_bef_invalid.json() == 'not a valid integer'
        assert self.rspnse_crt_user_invalid.json() == 'not a valid integer'
        assert self.rspnse_crt_account_invalid.json() == 'not a valid integer'
