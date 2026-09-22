from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class Order:
    id: int
    student_id: int
    items: list
    delivery_address_id: int
    payment_method_id: int
    total: int
    status: str
    idempotency_key: str | None = None
    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    def as_json(self) -> dict:
        return {
            "orderId": self.id,
            "status": self.status,
            "total": self.total,
            "estimatedMinutes": 30,
            "createdAt": self.created_at.isoformat()
        }