from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class MenuItem:

    id: int
    restaurant_id: int
    menu_id: int
    name: str
    description: str
    price: float
    available: bool

    idempotency_key: str | None = None

    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    def as_json(self) -> dict:
        """
        Public representation.

        Internal information such as idempotency_key and
        created_at is not exposed.
        """

        return {
            "id": self.id,
            "restaurantId": self.restaurant_id,
            "menuId": self.menu_id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "available": self.available
        }