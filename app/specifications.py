from decimal import Decimal
from app.domain import Order

# 1. Clase base Specification con operadores lógicos
class Specification:
    def is_satisfied_by(self, order: Order) -> bool:
        raise NotImplementedError

    def __and__(self, other: "Specification") -> "AndSpec":
        return AndSpec(self, other)

    def __or__(self, other: "Specification") -> "OrSpec":
        return OrSpec(self, other)

    def __invert__(self) -> "NotSpec":
        return NotSpec(self)


class AndSpec(Specification):
    def __init__(self, left: Specification, right: Specification):
        self.left = left
        self.right = right

    def is_satisfied_by(self, order: Order) -> bool:
        return self.left.is_satisfied_by(order) and self.right.is_satisfied_by(order)


class OrSpec(Specification):
    def __init__(self, left: Specification, right: Specification):
        self.left = left
        self.right = right

    def is_satisfied_by(self, order: Order) -> bool:
        return self.left.is_satisfied_by(order) or self.right.is_satisfied_by(order)


class NotSpec(Specification):
    def __init__(self, spec: Specification):
        self.spec = spec

    def is_satisfied_by(self, order: Order) -> bool:
        return not self.spec.is_satisfied_by(order)


# 2. Especificaciones Concretas
class MinimumAmountSpec(Specification):
    def __init__(self, threshold: Decimal):
        self.threshold = threshold

    def is_satisfied_by(self, order: Order) -> bool:
        return order.total.amount > self.threshold


class VIPCustomerSpec(Specification):
    def is_satisfied_by(self, order: Order) -> bool:
        return order.customer.is_vip


class MinimumUnitsSpec(Specification):
    def __init__(self, min_units: int):
        self.min_units = min_units

    def is_satisfied_by(self, order: Order) -> bool:
        return order.units >= self.min_units


class ActivePromotionSpec(Specification):
    def is_satisfied_by(self, order: Order) -> bool:
        return order.has_promotion


# 3. Reglas de descuento combinadas (Sección 8)
# Regla de 10%: VIP, total > 500, al menos 4 unidades y sin promoción activa
ten_percent_rule = (
    MinimumAmountSpec(Decimal("500"))
    & VIPCustomerSpec()
    & MinimumUnitsSpec(4)
    & ~ActivePromotionSpec()
)

# Regla de 5%: total > 5000 y sin promoción activa
five_percent_rule = (
    MinimumAmountSpec(Decimal("5000"))
    & ~ActivePromotionSpec()
)

# Combinación general con OR (si aplican ambas, la lógica del sistema prioriza el 10%)
combined_discount_rule = ten_percent_rule | five_percent_rule