from dataclasses import dataclass, field
from decimal import Decimal


@dataclass
class CheckoutInputDTO:
    shipping_name: str
    shipping_address: str
    shipping_city: str
    shipping_phone: str = ""
    notes: str = ""

    def validate(self) -> list[str]:
        errors = []
        if not self.shipping_name.strip():
            errors.append("Ad Soyad zorunludur.")
        if not self.shipping_address.strip():
            errors.append("Adres zorunludur.")
        if not self.shipping_city.strip():
            errors.append("Şehir zorunludur.")
        return errors

    @classmethod
    def from_post(cls, post_data: dict) -> "CheckoutInputDTO":
        return cls(
            shipping_name=post_data.get("shipping_name", "").strip(),
            shipping_address=post_data.get("shipping_address", "").strip(),
            shipping_city=post_data.get("shipping_city", "").strip(),
            shipping_phone=post_data.get("shipping_phone", "").strip(),
            notes=post_data.get("notes", "").strip(),
        )


@dataclass(frozen=True)
class OrderItemOutputDTO:
    product_id: int
    product_name: str
    unit_price: Decimal
    quantity: int
    line_total: Decimal


@dataclass(frozen=True)
class OrderOutputDTO:
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
