from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

from storium.views import RegisterView

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "giris/",
        auth_views.LoginView.as_view(template_name="registration/login.html"),
        name="login",
    ),
    path("kayit/", RegisterView.as_view(), name="register"),
    path("cikis/", auth_views.LogoutView.as_view(), name="logout"),
    path("", include("apps.catalog.urls", namespace="catalog")),
    path("", include("apps.cart.urls", namespace="cart")),
    path("siparis/", include("apps.orders.urls", namespace="orders")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
