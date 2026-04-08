from django.contrib import admin

from modules.orders.models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ["product", "product_name", "unit_price", "quantity", "line_total"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "status", "total_price", "created_at"]
    list_filter = ["status", "created_at"]
    search_fields = ["user__email", "shipping_name"]
    readonly_fields = ["total_price", "created_at", "updated_at"]
    inlines = [OrderItemInline]
    actions = ["mark_confirmed", "mark_shipped"]

    @admin.action(description="Seçili siparişleri Onayla")
    def mark_confirmed(self, request, queryset):
        from modules.notifications.services import EmailNotificationService
        from core.repositories.catalog_repository import DjangoProductRepository
        from core.repositories.order_repository import DjangoOrderRepository
        from core.services.order_service import OrderService

        svc = OrderService(
            order_repo=DjangoOrderRepository(),
            product_repo=DjangoProductRepository(),
            notification_service=EmailNotificationService(),
        )
        for order in queryset:
            if order.status == "pending":
                svc.update_order_status(order.id, "confirmed")

    @admin.action(description="Seçili siparişleri Kargoya Ver")
    def mark_shipped(self, request, queryset):
        from modules.notifications.services import EmailNotificationService
        from core.repositories.catalog_repository import DjangoProductRepository
        from core.repositories.order_repository import DjangoOrderRepository
        from core.services.order_service import OrderService

        svc = OrderService(
            order_repo=DjangoOrderRepository(),
            product_repo=DjangoProductRepository(),
            notification_service=EmailNotificationService(),
        )
        for order in queryset:
            if order.status == "confirmed":
                svc.update_order_status(order.id, "shipped")
