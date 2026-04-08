from decimal import Decimal
from typing import Any

from pydantic import BaseModel, ConfigDict, ValidationError, field_validator


def checkout_validation_messages(exc: ValidationError) -> list[str]:
    """Pydantic ValidationError → kullanıcıya gösterilecek kısa mesaj listesi."""
    out: list[str] = []
    for err in exc.errors():
        msg = err.get("msg", "Geçersiz veri.")
        if isinstance(msg, str) and msg.startswith("Value error, "):
            msg = msg[len("Value error, ") :]
        out.append(msg)
    return out


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

    @classmethod
    def from_post(cls, post_data: Any) -> "CheckoutInputDTO":
        def g(key: str) -> str:
            if hasattr(post_data, "get"):
                raw = post_data.get(key, "")
                return raw if isinstance(raw, str) else str(raw or "")
            return str((post_data or {}).get(key, "") or "")

        return cls.model_validate(
            {
                "shipping_name": g("shipping_name"),
                "shipping_address": g("shipping_address"),
                "shipping_city": g("shipping_city"),
                "shipping_phone": g("shipping_phone"),
                "notes": g("notes"),
            }
        )


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
