from fastapi.testclient import TestClient
from app.database import get_db, Base
from app.main import app
from app import schemas
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.oauth2 import create_access_token
from app import models
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


@pytest.fixture
def test_createuser(client):
    user_data = {"Email": "erty@gmail.com", "Password": "1234"}
    res = client.post("/sqlalchemy/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['Password'] = user_data['Password']
    return new_user


@pytest.fixture
def test_createuser2(client):
    user_data = {"Email": "ert123@gmail.com", "Password": "password123"}
    res = client.post("/sqlalchemy/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['Password'] = user_data['Password']
    return new_user


@pytest.fixture
def token(test_createuser):
    return create_access_token({"user_id": test_createuser['Id']})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client


@pytest.fixture
def test_posts(test_createuser, session, test_createuser2):
    posts_data = [{
        "Title": "first title",
        "Content": "first content",
        "User_Id": test_createuser['Id']
    }, {
        "Title": "2nd title",
        "Content": "2nd content",
        "User_Id": test_createuser['Id']
    },
        {
        "Title": "3rd title",
        "Content": "3rd content",
        "User_Id": test_createuser['Id']
    },
        {
        "Title": "4th title",
        "Content": "4th content",
        "User_Id": test_createuser2['Id']
    }]

    def create_post_model(post):
        return models.Post(**post)

    post_map = map(create_post_model, posts_data)
    posts = list(post_map)

    session.add_all(posts)
    # session.add_all([models.Post(title="first title", content="first content", owner_id=test_user['id']),
    #                 models.Post(title="2nd title", content="2nd content", owner_id=test_user['id']), models.Post(title="3rd title", content="3rd content", owner_id=test_user['id'])])
    session.commit()
    posts = session.query(models.Post).all()
    return posts


@pytest.fixture()
def test_vote(test_posts, session, test_createuser):
    new_vote = models.Vote(
        Post_Id=test_posts[3].Id, User_Id=test_createuser['Id'])
    session.add(new_vote)
    session.commit()
