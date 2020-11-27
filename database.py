from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, database_exists

Base = declarative_base()
DATABASE = "sqlite:///./bank.db"
TEST_DATABASE = "sqlite:///./test.db"


def database_session_creator(url: str):
    '''
    Creates a local session and database engine for the main database.
    '''
    engine = create_engine(url, connect_args={"check_same_thread": False})

    if not database_exists(DATABASE):
        create_database(DATABASE)
    else:
        engine.connect()
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal, engine


def get_db():
    '''
    A standard fastapi implementation of get db. Used in the api endpoints
    alongside the Depends function.
    '''
    try:
        SessionLocal, engine = database_session_creator(DATABASE)
        db = SessionLocal()
        yield db

    finally:
        db.close()


SessionLocal, engine = database_session_creator(DATABASE)
