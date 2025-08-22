from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)

def test_crear_pedido_vacio():
    response = client.post("/orders/", json={"customer_name": "Juan", "items": []})
    assert response.status_code == 200
    assert response.json()["status"] == 400

def test_crear_pedido_precio_invalido():
    response = client.post("/orders/", json={
        "customer_name": "Ana",
        "items": [{"name": "Producto", "price": 0}]
    })
    assert response.status_code == 200
    assert response.json()["status"] == 400

def test_crear_pedido_valido():
    response = client.post("/orders/", json={
        "customer_name": "Pedro",
        "items": [{"name": "Producto", "price": 10}]
    })
    assert response.status_code == 200
    assert response.json()["status"] == 201
