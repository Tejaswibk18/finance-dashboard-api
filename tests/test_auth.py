from fastapi.testclient import TestClient
from app.main import app
import uuid

client = TestClient(app)


def test_register():
    email = f"test_{uuid.uuid4()}@test.com"

    response = client.post("/auth/register", json={
        "email": email,
        "password": "Password@123",
        "role": "admin"
    })

    assert response.status_code == 200
    assert response.json()["status"] == "success"


def test_duplicate_user():
    email = f"dup_{uuid.uuid4()}@test.com"

    # first register
    client.post("/auth/register", json={
        "email": email,
        "password": "Password@123",
        "role": "admin"
    })

    # second register
    response = client.post("/auth/register", json={
        "email": email,
        "password": "Password@123",
        "role": "admin"
    })

    assert response.json()["status"] == "failed"
    assert "already exists" in response.json()["message"]


def test_login_invalid():
    response = client.post("/auth/login", json={
        "email": "wrong@test.com",
        "password": "Wrong@123"
    })

    assert response.json()["status"] == "failed"