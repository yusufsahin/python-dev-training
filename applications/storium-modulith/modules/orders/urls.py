from django.urls import path

from modules.orders import views

app_name = "orders"

urlpatterns = [
    path("checkout/", views.CheckoutView.as_view(), name="checkout"),
    path("tamamlandi/<int:order_id>/", views.OrderConfirmView.as_view(), name="order_confirm"),
    path("", views.OrderListView.as_view(), name="order_list"),
    path("<int:order_id>/", views.OrderDetailView.as_view(), name="order_detail"),
]
