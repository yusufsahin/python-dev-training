from django.urls import path

from apps.cart import views

app_name = "cart"

urlpatterns = [
    path("sepet/", views.CartDetailView.as_view(), name="cart_detail"),
    path("sepet/ekle/", views.AddToCartView.as_view(), name="cart_add"),
    path("sepet/guncelle/", views.UpdateCartView.as_view(), name="cart_update"),
    path("sepet/sil/<int:product_id>/", views.RemoveFromCartView.as_view(), name="cart_remove"),
    path("sepet/temizle/", views.ClearCartView.as_view(), name="cart_clear"),
]
