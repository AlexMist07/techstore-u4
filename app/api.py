from fastapi import FastAPI, HTTPException
from cargar_csv import load_fixture
from app.domain import InvalidOrderTransition, InvalidOrderData

app = FastAPI(title="TechStore U4", version="1.0")

# Cargamos los fixtures en memoria al iniciar la aplicación
orders = load_fixture()

@app.get("/orders/{order_id}")
def get_order(order_id: str):
    order = orders.get(order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="El pedido no existe")
    return {
        "id": order.id,
        "customer_id": order.customer.id,
        "status": order.status.value,
        "units": order.units,
        "total": float(order.total.amount),
        "has_promotion": order.has_promotion
    }

@app.post("/orders/{order_id}/confirm")
def confirm_order(order_id: str):
    order = orders.get(order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="El pedido no existe")
    try:
        order.confirm()
    except InvalidOrderTransition as exc:
        raise HTTPException(status_code=409, detail=str(exc))
    except InvalidOrderData as exc:
        raise HTTPException(status_code=422, detail=str(exc))
    return {"id": order.id, "status": order.status.value, "events": [e.name for e in order.events]}

@app.post("/orders/{order_id}/ship")
def ship_order(order_id: str, tracking_number: str = "GUIA-123"):
    order = orders.get(order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="El pedido no existe")
    try:
        order.ship(tracking_number)
    except InvalidOrderTransition as exc:
        raise HTTPException(status_code=409, detail=str(exc))
    except InvalidOrderData as exc:
        raise HTTPException(status_code=422, detail=str(exc))
    return {"id": order.id, "status": order.status.value, "events": [e.name for e in order.events]}

@app.post("/orders/{order_id}/cancel")
def cancel_order(order_id: str, reason: str = "Cliente ausente"):
    order = orders.get(order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="El pedido no existe")
    try:
        order.cancel(reason)
    except InvalidOrderTransition as exc:
        raise HTTPException(status_code=409, detail=str(exc))
    except InvalidOrderData as exc:
        raise HTTPException(status_code=422, detail=str(exc))
    return {"id": order.id, "status": order.status.value, "events": [e.name for e in order.events]}