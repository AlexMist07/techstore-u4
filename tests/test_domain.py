import pytest
from decimal import Decimal
from app.domain import Money, InvalidOrderData, InvalidOrderTransition, OrderItem, Customer, Order, OrderStatus
from app.specifications import MinimumAmountSpec, VIPCustomerSpec, MinimumUnitsSpec, ActivePromotionSpec
from cargar_csv import load_fixture

def test_money_negativo():
    with pytest.raises(InvalidOrderData):
        Money(Decimal("-1"))

def test_pedido_o001_inicia_draft():
    orders = load_fixture()
    assert orders["O001"].status.value == "DRAFT"
    assert orders["O001"].units == 4
    assert orders["O001"].total.amount == Decimal("2100.00")

def test_limite_20_unidades():
    customer = Customer(id="C999", is_vip=True, active=True)
    order = Order(customer=customer, id="TEST-99")
    item_pesado = OrderItem(sku="SKU999", quantity=21, unit_price=Money(Decimal("100")))
    
    with pytest.raises(Exception):
        order.add_item(item_pesado)

def test_transicion_doble_confirmacion():
    orders = load_fixture()
    order = orders["O013"]
    
    # Primera confirmación (válida)
    order.confirm()
    assert order.status == OrderStatus.CONFIRMED
    assert len(order.events) == 1
    assert order.events[0].name == "OrderConfirmed"
    
    # Segunda confirmación (debe fallar con InvalidOrderTransition)
    with pytest.raises(InvalidOrderTransition):
        order.confirm()
    
    # El número de eventos no debe aumentar
    assert len(order.events) == 1

def test_envio_sin_guia():
    orders = load_fixture()
    order = orders["O002"]
    order.confirm()
    
    # Intentar enviar sin número de guía debe lanzar error
    with pytest.raises(InvalidOrderData):
        order.ship("")

def test_especificacion_descuento_vip():
    orders = load_fixture()
    order = orders["O001"] # Cliente VIP, total > 500, unidades >= 4, sin promoción activa
    
    ten_percent = (
        MinimumAmountSpec(Decimal("500"))
        & VIPCustomerSpec()
        & MinimumUnitsSpec(4)
        & ~ActivePromotionSpec()
    )
    
    assert ten_percent.is_satisfied_by(order) is True