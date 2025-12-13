from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app import models

client = TestClient(app)


def clear_users_table():
    db = SessionLocal()
    db.query(models.User).delete()
    db.commit()
    db.close()


def test_user_can_register():
    clear_users_table()  # 🔑 THIS WAS MISSING OR NOT SAVED

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


def test_register_fails_if_username_exists():
    clear_users_table()  # 🔑 clean DB again

    client.post(
        "/api/auth/register",
        json={
            "username": "duplicateuser",
            "password": "pass123"
        }
    )

    response = client.post(
        "/api/auth/register",
        json={
            "username": "duplicateuser",
            "password": "pass456"
        }
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Username already exists"
