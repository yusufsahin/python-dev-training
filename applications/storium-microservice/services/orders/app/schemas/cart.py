from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class CartItemDTO(BaseModel):
    model_config = ConfigDict(frozen=True)

    product_id: int
    name: str
    price: Decimal
    quantity: int = Field(ge=1)
    image_url: Optional[str] = None


class CartDTO(BaseModel):
    model_config = ConfigDict(frozen=True)

    items: list[CartItemDTO] = Field(default_factory=list)
    total_price: Decimal = Decimal("0")
    item_count: int = 0
    unique_item_count: int = 0
