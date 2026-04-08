from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View

from core.exceptions.domain_exceptions import OutOfStockException, ProductNotFoundException
from core.repositories.catalog_repository import DjangoProductRepository
from core.services.cart_service import CartService


class CartDetailView(View):
    template_name = "cart/cart_detail.html"

    def get(self, request):
        service = CartService(
            product_repo=DjangoProductRepository(),
            session=request.session,
        )
        cart = service.get_cart()
        return render(request, self.template_name, {"cart": cart})


class AddToCartView(View):
    def post(self, request):
        product_id = int(request.POST.get("product_id"))
        quantity = int(request.POST.get("quantity", 1))
        service = CartService(product_repo=DjangoProductRepository(), session=request.session)
        try:
            service.add_item(product_id, quantity)
            messages.success(request, "Ürün sepete eklendi.")
        except ProductNotFoundException:
            messages.error(request, "Ürün bulunamadı.")
        except OutOfStockException as e:
            messages.warning(request, str(e))
        next_url = request.POST.get("next") or reverse("cart:cart_detail")
        return redirect(next_url)


class UpdateCartView(View):
    def post(self, request):
        product_id = int(request.POST.get("product_id"))
        quantity = int(request.POST.get("quantity", 0))
        service = CartService(product_repo=DjangoProductRepository(), session=request.session)
        try:
            service.update_item(product_id, quantity)
            if quantity > 0:
                messages.success(request, "Sepet güncellendi.")
            else:
                messages.info(request, "Ürün sepetten çıkarıldı.")
        except OutOfStockException as e:
            messages.warning(request, str(e))
        return redirect("cart:cart_detail")


class RemoveFromCartView(View):
    def post(self, request, product_id):
        service = CartService(product_repo=DjangoProductRepository(), session=request.session)
        service.remove_item(product_id)
        messages.info(request, "Ürün sepetten çıkarıldı.")
        return redirect("cart:cart_detail")


class ClearCartView(View):
    def post(self, request):
        service = CartService(product_repo=DjangoProductRepository(), session=request.session)
        service.clear_cart()
        messages.info(request, "Sepet temizlendi.")
        return redirect("cart:cart_detail")
