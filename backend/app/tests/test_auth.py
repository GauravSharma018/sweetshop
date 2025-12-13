from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_user_can_register():
    response = client.post(
        "/api/auth/register",
        json={
            "username": "testuser",
            "password": "testpass"
        }
    )

    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser"
