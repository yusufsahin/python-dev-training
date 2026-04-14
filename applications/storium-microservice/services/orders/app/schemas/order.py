from decimal import Decimal

from pydantic import BaseModel, ConfigDict, field_validator


class CheckoutInputDTO(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    shipping_name: str
    shipping_address: str
    shipping_city: str
    shipping_phone: str = ""
    notes: str = ""

    @field_validator("shipping_name")
    @classmethod
    def _shipping_name(cls, v: str) -> str:
        if not v:
            raise ValueError("Ad Soyad zorunludur.")
        return v

    @field_validator("shipping_address")
    @classmethod
    def _shipping_address(cls, v: str) -> str:
        if not v:
            raise ValueError("Adres zorunludur.")
        return v

    @field_validator("shipping_city")
    @classmethod
    def _shipping_city(cls, v: str) -> str:
        if not v:
            raise ValueError("Şehir zorunludur.")
        return v


class OrderItemOutputDTO(BaseModel):
    model_config = ConfigDict(frozen=True)

    product_id: int
    product_name: str
    unit_price: Decimal
    quantity: int
    line_total: Decimal


class OrderOutputDTO(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: int
    status: str
    status_display: str
    total_price: Decimal
    shipping_name: str
    shipping_address: str
    shipping_city: str
    shipping_phone: str
    notes: str
    items: list[OrderItemOutputDTO]
    created_at: str
    updated_at: str
