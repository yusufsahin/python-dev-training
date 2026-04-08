from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View

from modules.notifications.services import EmailNotificationService
from pydantic import ValidationError

from core.dtos.order_dtos import CheckoutInputDTO, checkout_validation_messages
from core.exceptions.domain_exceptions import (
    EmptyCartException,
    OrderAccessDeniedException,
    OrderNotFoundException,
    OutOfStockException,
)
from core.repositories.catalog_repository import DjangoProductRepository
from core.repositories.order_repository import DjangoOrderRepository
from core.services.cart_service import CartService
from core.services.order_service import OrderService


def _make_order_service() -> OrderService:
    return OrderService(
        order_repo=DjangoOrderRepository(),
        product_repo=DjangoProductRepository(),
        notification_service=EmailNotificationService(),
    )


def _make_cart_service(session) -> CartService:
    return CartService(
        product_repo=DjangoProductRepository(),
        session=session,
    )


@method_decorator(login_required, name="dispatch")
class CheckoutView(View):
    template_name = "orders/checkout.html"

    def get(self, request):
        cart_service = _make_cart_service(request.session)
        cart = cart_service.get_cart()
        if not cart.items:
            messages.warning(request, "Sepetiniz boş.")
            return redirect("cart:cart_detail")
        return render(request, self.template_name, {"cart": cart})

    def post(self, request):
        cart_service = _make_cart_service(request.session)
        cart = cart_service.get_cart()
        if not cart.items:
            return redirect("cart:cart_detail")

        try:
            checkout_input = CheckoutInputDTO.from_post(request.POST)
        except ValidationError as exc:
            for error in checkout_validation_messages(exc):
                messages.error(request, error)
            return render(request, self.template_name, {"cart": cart})

        order_service = _make_order_service()
        try:
            order_dto = order_service.create_order(
                user_id=request.user.id,
                cart_dto=cart,
                checkout_input=checkout_input,
            )
        except EmptyCartException:
            return redirect("cart:cart_detail")
        except OutOfStockException as e:
            messages.error(request, str(e))
            return render(request, self.template_name, {"cart": cart})

        cart_service.clear_cart()
        return redirect("orders:order_confirm", order_id=order_dto.id)


@method_decorator(login_required, name="dispatch")
class OrderConfirmView(View):
    template_name = "orders/order_confirm.html"

    def get(self, request, order_id):
        order_service = _make_order_service()
        try:
            order = order_service.get_order_detail(order_id, request.user.id)
        except (OrderNotFoundException, OrderAccessDeniedException):
            raise Http404 from None
        return render(request, self.template_name, {"order": order})


@method_decorator(login_required, name="dispatch")
class OrderListView(View):
    template_name = "orders/order_list.html"

    def get(self, request):
        order_service = _make_order_service()
        orders = order_service.get_user_orders(request.user.id)
        return render(request, self.template_name, {"orders": orders})


@method_decorator(login_required, name="dispatch")
class OrderDetailView(View):
    template_name = "orders/order_detail.html"

    def get(self, request, order_id):
        order_service = _make_order_service()
        try:
            order = order_service.get_order_detail(order_id, request.user.id)
        except OrderNotFoundException:
            raise Http404 from None
        except OrderAccessDeniedException:
            messages.error(request, "Bu siparişe erişim yetkiniz yok.")
            return redirect("orders:order_list")
        return render(request, self.template_name, {"order": order})
