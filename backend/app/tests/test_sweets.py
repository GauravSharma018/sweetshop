from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app import models
from app.auth import hash_password

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


def test_authenticated_user_can_list_sweets():
    token = register_and_login()

    # Add a sweet first
    client.post(
        "/api/sweets",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Barfi",
            "category": "Indian",
            "price": 20.0,
            "quantity": 50
        }
    )

    response = client.get(
        "/api/sweets",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["name"] == "Barfi"


def test_user_can_search_sweets_by_category():
    token = register_and_login()

    # Add sweets
    client.post(
        "/api/sweets",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Ladoo",
            "category": "Indian",
            "price": 10,
            "quantity": 100
        }
    )

    client.post(
        "/api/sweets",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Brownie",
            "category": "Bakery",
            "price": 30,
            "quantity": 20
        }
    )

    response = client.get(
        "/api/sweets/search?category=Indian",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Ladoo"


def test_user_can_purchase_sweet_and_quantity_decreases():
    token = register_and_login()

    # Create sweet
    create_resp = client.post(
        "/api/sweets",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Jalebi",
            "category": "Indian",
            "price": 15,
            "quantity": 2
        }
    )

    sweet_id = create_resp.json()["id"]

    # Purchase once
    response = client.post(
        f"/api/sweets/{sweet_id}/purchase",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["quantity"] == 1


def test_purchase_fails_when_out_of_stock():
    token = register_and_login()

    # Create sweet with zero quantity
    create_resp = client.post(
        "/api/sweets",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Rasgulla",
            "category": "Indian",
            "price": 20,
            "quantity": 0
        }
    )

    sweet_id = create_resp.json()["id"]

    response = client.post(
        f"/api/sweets/{sweet_id}/purchase",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Sweet out of stock"


def test_admin_can_restock_sweet():
    clear_tables()

    # Create admin user manually
    db = SessionLocal()
    admin = models.User(
        username="admin",
         password_hash=hash_password("adminpass"),
        is_admin=True
    )
    db.add(admin)
    db.commit()
    db.close()

    # Login admin
    response = client.post(
        "/api/auth/login",
        json={"username": "admin", "password": "adminpass"}
    )
    token = response.json()["access_token"]

    # Create sweet
    create_resp = client.post(
        "/api/sweets",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Kaju Katli",
            "category": "Indian",
            "price": 50,
            "quantity": 5
        }
    )
    sweet_id = create_resp.json()["id"]

    # Restock
    restock_resp = client.post(
        f"/api/sweets/{sweet_id}/restock",
        headers={"Authorization": f"Bearer {token}"},
        json={"quantity": 10}
    )

    assert restock_resp.status_code == 200
    assert restock_resp.json()["quantity"] == 15


def test_non_admin_cannot_restock():
    token = register_and_login()

    create_resp = client.post(
        "/api/sweets",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Peda",
            "category": "Indian",
            "price": 30,
            "quantity": 5
        }
    )
    sweet_id = create_resp.json()["id"]

    response = client.post(
        f"/api/sweets/{sweet_id}/restock",
        headers={"Authorization": f"Bearer {token}"},
        json={"quantity": 5}
    )

    assert response.status_code == 403
    