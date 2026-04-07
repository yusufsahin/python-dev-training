from dataclasses import dataclass
from decimal import Decimal
from typing import Optional


@dataclass(frozen=True)
class CartItemDTO:
    product_id: int
    name: str
    price: Decimal
    quantity: int
    image_url: Optional[str]

    @property
    def line_total(self) -> Decimal:
        return self.price * self.quantity


@dataclass(frozen=True)
class CartDTO:
    items: list[CartItemDTO]
    total_price: Decimal
    item_count: int
    unique_item_count: int
