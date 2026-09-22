from models import MenuItem


_items: dict[int, MenuItem] = {}

_by_key: dict[str, int] = {}

_next_id = 1


def create(
    restaurant_id,
    menu_id,
    name,
    description,
    price,
    available,
    key=None
):

    global _next_id

    item = MenuItem(
        id=_next_id,
        restaurant_id=restaurant_id,
        menu_id=menu_id,
        name=name,
        description=description,
        price=price,
        available=available,
        idempotency_key=key
    )

    _items[item.id] = item

    if key:
        _by_key[key] = item.id

    _next_id += 1

    return item


def find(item_id):

    return _items.get(item_id)


def find_by_key(key):

    item_id = _by_key.get(key)

    if item_id is None:
        return None

    return _items.get(item_id)


def find_by_restaurant(restaurant_id):

    return [
        item
        for item in _items.values()
        if item.restaurant_id == restaurant_id
    ]


def search(text):

    text = text.lower()

    return [
        item
        for item in _items.values()
        if text in item.name.lower()
        or text in item.description.lower()
    ]


def reset():

    global _next_id

    _items.clear()
    _by_key.clear()
    _next_id = 1