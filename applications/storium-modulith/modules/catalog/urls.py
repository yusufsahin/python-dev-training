from django.urls import path

from modules.catalog import views

app_name = "catalog"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("kategori/<slug:slug>/", views.CategoryProductListView.as_view(), name="category_detail"),
    path("urun/<slug:slug>/", views.ProductDetailView.as_view(), name="product_detail"),
    path("arama/", views.ProductSearchView.as_view(), name="product_search"),
]
