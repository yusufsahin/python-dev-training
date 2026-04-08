from decimal import Decimal

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models


class OrderStatus(models.TextChoices):
    PENDING = "pending", "Beklemede"
    CONFIRMED = "confirmed", "Onaylandı"
    SHIPPED = "shipped", "Kargoya Verildi"
    DELIVERED = "delivered", "Teslim Edildi"
    CANCELLED = "cancelled", "İptal Edildi"


class Order(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="orders",
    )
    status = models.CharField(
        max_length=20,
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING,
    )
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_name = models.CharField(max_length=200)
    shipping_address = models.TextField()
    shipping_city = models.CharField(max_length=100)
    shipping_phone = models.CharField(max_length=20, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"Sipariş #{self.id} — {self.user} — {self.get_status_display()}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
    )
    product = models.ForeignKey(
        "catalog.Product",
        on_delete=models.PROTECT,
    )
    product_name = models.CharField(max_length=255)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    def __str__(self) -> str:
        return f"{self.product_name} x{self.quantity}"

    @property
    def line_total(self) -> Decimal:
        return self.unit_price * self.quantity
