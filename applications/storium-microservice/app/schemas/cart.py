from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, computed_field


class CartItemDTO(BaseModel):
    model_config = ConfigDict(frozen=True)

    product_id: int
    name: str
    price: Decimal
    quantity: int
    image_url: Optional[str] = None

    @computed_field
    def line_total(self) -> Decimal:
        return self.price * self.quantity


class CartDTO(BaseModel):
    model_config = ConfigDict(frozen=True)

    items: list[CartItemDTO]
    total_price: Decimal
    item_count: int
    unique_item_count: int


class CartItemAdd(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    product_id: int
    quantity: int = Field(default=1, ge=1)
