from fastapi.testclient import TestClient
from app.api import app

client = TestClient(app)

def test_get_order_success():
    response = client.get("/orders/O001")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "O001"
    assert data["status"] == "DRAFT"

def test_get_order_not_found():
    response = client.get("/orders/X999")
    assert response.status_code == 404
    assert response.json()["detail"] == "El pedido no existe"

def test_confirm_order_success():
    response = client.post("/orders/O015/confirm")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "CONFIRMED"
    assert "OrderConfirmed" in data["events"]

def test_confirm_order_conflict():
    # Confirmamos O016 por primera vez
    client.post("/orders/O016/confirm")
    # Segunda confirmación debe arrojar conflicto (409)
    response = client.post("/orders/O016/confirm")
    assert response.status_code == 409