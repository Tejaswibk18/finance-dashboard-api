from fastapi.testclient import TestClient
from app.main import app
import uuid

client = TestClient(app)


def get_token(role="admin"):
    email = f"user_{uuid.uuid4()}@test.com"

    client.post("/auth/register", json={
        "email": email,
        "password": "Password@123",
        "role": role
    })

    res = client.post("/auth/login", json={
        "email": email,
        "password": "Password@123"
    })

    return res.json()["data"]["access_token"]


def test_create_record_admin():
    token = get_token("admin")

    response = client.post(
        "/records",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "amount": 100,
            "type": "income",
            "category": "salary"
        }
    )

    assert response.status_code == 200
    assert response.json()["status"] == "success"


def test_create_record_viewer_forbidden():
    token = get_token("viewer")

    response = client.post(
        "/records",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "amount": 100,
            "type": "income",
            "category": "salary"
        }
    )

    assert response.status_code == 403


def test_invalid_amount():
    token = get_token("admin")

    response = client.post(
        "/records",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "amount": -10,
            "type": "income",
            "category": "salary"
        }
    )

    assert response.status_code == 400


def test_invalid_object_id():
    token = get_token("admin")

    response = client.delete(
        "/records/invalid_id",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 400