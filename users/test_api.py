import pytest

from main import app
from app import crud, pwd
from app.database import SessionLocal 
from fastapi.testclient import TestClient
from typing import List

client = TestClient(app)

def create_user(session, emails: List[str]):
    for email in emails:
        user = crud.get_user_by_email(session, email)
        if user is None:
            user = crud.create_user(session, name=email, email=email, password_hash=pwd.password_hash("test"))
        yield user 
                
@pytest.fixture(name="user")
def user_fixture():
    with SessionLocal() as session:
        for user in create_user(session, ["carol@gmail.com"]):
            yield user

@pytest.fixture(name="users")
def users_fixture():
    with SessionLocal() as session:
        users = []
        for user in create_user(session, ["carol@gmail.com", "alice@gmail.com", "bob@gmail.com"]):
            users.append(user)
        yield users

def test_auth_by_pass(user):
    response = client.post(
        "/auth/password",
        json={"username": user.email, "password": "test"}

    )
    assert response.status_code == 200
    assert True == response.json()["ok"]
    assert response.json()["token"] is not None

def test_auth_wrong_pass(user):
    response = client.post(
        "/auth/password",
        json={"username": user.email, "password": "__"}

    )
    assert response.status_code == 200
    assert response.json()["token"] is None
    assert False == response.json()["ok"]

def test_refresh_token(user):
    response = client.post(
        "/auth/password",
        json={"username": user.email, "password": "test"}
    )
    assert response.status_code == 200

    token = response.json()["token"]
    response = client.post(
        "/token/refresh",
        data={"token": token}
    )
    
    assert response.status_code == 200
    json = response.json()
    assert True == json["ok"]
    assert json["token"] is not None

def test_users(users):
    response = client.post(
        "/users",
        json={}
    )
    assert response.status_code == 200
    json = response.json()
    assert len(users) == len(json["items"])

def test_users_by_ids(users):
    response = client.post(
        "/users",
        json={"ids": [users[0].user_id]}
    )
    assert response.status_code == 200
    json = response.json()
    assert len(json["items"]) == 1 
