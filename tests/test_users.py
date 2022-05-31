from fastapi import FastAPI
from app import schemas
from jose import jwt
from .database import client, session
from app.config import settings
import pytest

app = FastAPI()


@pytest.fixture
def test_createuser(client):
    user_data = {"Email": "erty@gmail.com", "Password": "1234"}
    res = client.post("/sqlalchemy/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['Password'] = user_data['Password']
    return new_user


def test_root(client):
    res = client.get("/")
    print(res.json().get('Message'))
    assert res.json().get('Message') == 'Hello World!'
    assert res.status_code == 200


def test_create_user(client):
    res = client.post("/sqlalchemy/users/",
                      json={"Email": "erty@gmail.com", "Password": "1234"})
    new_user = schemas.UserResponse(**res.json())
    print(new_user)
    assert res.status_code == 201


def test_login_user(client, test_createuser):
    res = client.post("/login",
                      data={"username": test_createuser['Email'], "password": test_createuser['Password']})
    logintoken = schemas.TokenResponse(**res.json())
    payload = jwt.decode(logintoken.Access_Token,
                         settings.Secret_Key, algorithms=[settings.Algorithm])
    id = payload.get("user_id")
    assert id == int(test_createuser['Id'])
    assert res.status_code == 200
