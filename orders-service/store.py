from models import Order


_orders: dict[int, Order] = {}
_idempotency_keys: dict[str, int] = {}
_next_id = 1


def create_order(
    student_id: int,
    items: list,
    delivery_address_id: int,
    payment_method_id: int,
    total: int,
    status: str,
    idempotency_key: str | None = None
) -> Order:
    global _next_id

    order = Order(
        id=_next_id,
        student_id=student_id,
        items=items,
        delivery_address_id=delivery_address_id,
        payment_method_id=payment_method_id,
        total=total,
        status=status,
        idempotency_key=idempotency_key
    )

    _orders[order.id] = order

    if idempotency_key:
        _idempotency_keys[idempotency_key] = order.id

    _next_id += 1

    return order


def find_order(order_id: int) -> Order | None:
    return _orders.get(order_id)


def find_by_status(status: str) -> list[Order]:
    return [
        order
        for order in _orders.values()
        if order.status == status
    ]


def find_by_idempotency_key(key: str) -> Order | None:
    order_id = _idempotency_keys.get(key)

    if order_id is None:
        return None

    return _orders.get(order_id)


def cancel_order(order: Order) -> Order:
    order.status = "cancelled"
    return order
def find_all() -> list[Order]:
    return list(_orders.values())