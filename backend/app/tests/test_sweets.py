from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app import models

client = TestClient(app)


def clear_tables():
    db = SessionLocal()
    db.query(models.Sweet).delete()
    db.query(models.User).delete()
    db.commit()
    db.close()


def register_and_login():
    clear_tables()

    client.post(
        "/api/auth/register",
        json={"username": "admin", "password": "adminpass"}
    )

    response = client.post(
        "/api/auth/login",
        json={"username": "admin", "password": "adminpass"}
    )

    return response.json()["access_token"]


def test_add_sweet_requires_authentication():
    clear_tables()

    response = client.post(
        "/api/sweets",
        json={
            "name": "Ladoo",
            "category": "Indian",
            "price": 10,
            "quantity": 100
        }
    )

    assert response.status_code == 401

def test_authenticated_user_can_add_sweet():
    token = register_and_login()

    response = client.post(
        "/api/sweets",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "name": "Ladoo",
            "category": "Indian",
            "price": 10.0,
            "quantity": 100
        }
    )

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Ladoo"
    assert data["quantity"] == 100
