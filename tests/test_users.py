from app import schemas
from jose import jwt
from app.config import settings
import pytest


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


@pytest.mark.parametrize("email, password, status_code", [
    ('wrongemail@gmail.com', 'password123', 403),
    ('sanjeev@gmail.com', 'wrongpassword', 403),
    ('wrongemail@gmail.com', 'wrongpassword', 403),
    (None, 'password123', 422),
    ('sanjeev@gmail.com', None, 422)])
def test_incorrect_login(client, email, password, status_code):
    res = client.post("/login",
                      data={"username": email, "password": password})
    assert res.status_code == status_code
    # assert res.json().get('detail') == 'Invalid Credential'
