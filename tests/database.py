from fastapi.testclient import TestClient
from app.database import get_db, Base
from app.main import app
from app import schemas
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pytest

SQLALCHEMY_DATABSE_URL = f'postgresql://{settings.Database_Username}:{settings.Database_Password}@{settings.Database_Hostname}:{settings.Database_Port}/{settings.Database_Name}_Test'


engine = create_engine(SQLALCHEMY_DATABSE_URL)

SessionLocal_Test = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)

# The below line builds all the models and creates the tables. NB: the table should be created already on pgadmin before running this file.
# Base.metadata.create_all(bind=engine)


# def get_test_db():
#     db = SessionLocal_Test()
#     try:
#         yield db
#     finally:
#         db.close()


# overides the normal get_db session
# app.dependency_overrides[get_db] = get_test_db


# client = TestClient(app)

# instead of running the above, you can do below and pass in the fixture function as a variable in the test functions
# @pytest.fixture
# def client():
#     return TestClient(app)

# or do the below to create tables before running tests and drop tables after the testing

# session, refers to the database instance
@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal_Test()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    def get_test_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = get_test_db

    yield TestClient(app)
