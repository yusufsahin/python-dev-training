# 08 — Orders (Sipariş) Modülü

## Kapsam
- Checkout (ödeme/teslimat bilgileri formu)
- Sipariş onay sayfası
- Kullanıcının sipariş listesi
- Sipariş detay sayfası
- Tüm order view'ları `@login_required`

---

## URL Yapısı (apps/orders/urls.py)

```python
from django.urls import path
from apps.orders import views

app_name = 'orders'

urlpatterns = [
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('tamamlandi/<int:order_id>/', views.OrderConfirmView.as_view(), name='order_confirm'),
    path('', views.OrderListView.as_view(), name='order_list'),
    path('<int:order_id>/', views.OrderDetailView.as_view(), name='order_detail'),
]
```

Ana `storium/urls.py`'de:
```python
path('siparis/', include('apps.orders.urls', namespace='orders')),
```

---

## Views (apps/orders/views.py)

Tüm view'lar `@method_decorator(login_required, name='dispatch')` ile korunur.

### Ortak Service Fabrikası

```python
from apps.notifications.services import EmailNotificationService
from core.repositories.catalog_repository import DjangoProductRepository
from core.repositories.order_repository import DjangoOrderRepository

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
```

### CheckoutView (GET + POST)

```python
@method_decorator(login_required, name='dispatch')
class CheckoutView(View):
    template_name = 'orders/checkout.html'

    def get(self, request):
        cart_service = _make_cart_service(request.session)
        cart = cart_service.get_cart()
        if not cart.items:
            messages.warning(request, "Sepetiniz boş.")
            return redirect('cart:cart_detail')
        return render(request, self.template_name, {'cart': cart})

    def post(self, request):
        cart_service = _make_cart_service(request.session)
        cart = cart_service.get_cart()
        if not cart.items:
            return redirect('cart:cart_detail')

        checkout_input = CheckoutInputDTO.from_post(request.POST)
        errors = checkout_input.validate()
        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, self.template_name, {'cart': cart})

        order_service = _make_order_service()
        try:
            order_dto = order_service.create_order(
                user_id=request.user.id,
                cart_dto=cart,
                checkout_input=checkout_input,
            )
        except EmptyCartException:
            return redirect('cart:cart_detail')
        except OutOfStockException as e:
            messages.error(request, str(e))
            return render(request, self.template_name, {'cart': cart})

        # Sipariş başarılı: sepeti temizle, onay sayfasına yönlendir
        cart_service.clear_cart()
        return redirect('orders:order_confirm', order_id=order_dto.id)
```

### OrderConfirmView (GET)

```python
@method_decorator(login_required, name='dispatch')
class OrderConfirmView(View):
    template_name = 'orders/order_confirm.html'

    def get(self, request, order_id):
        order_service = _make_order_service()
        try:
            order = order_service.get_order_detail(order_id, request.user.id)
        except (OrderNotFoundException, OrderAccessDeniedException):
            raise Http404
        return render(request, self.template_name, {'order': order})
```

### OrderListView (GET)

```python
@method_decorator(login_required, name='dispatch')
class OrderListView(View):
    template_name = 'orders/order_list.html'

    def get(self, request):
        order_service = _make_order_service()
        orders = order_service.get_user_orders(request.user.id)
        return render(request, self.template_name, {'orders': orders})
```

### OrderDetailView (GET)

```python
@method_decorator(login_required, name='dispatch')
class OrderDetailView(View):
    template_name = 'orders/order_detail.html'

    def get(self, request, order_id):
        order_service = _make_order_service()
        try:
            order = order_service.get_order_detail(order_id, request.user.id)
        except OrderNotFoundException:
            raise Http404
        except OrderAccessDeniedException:
            messages.error(request, "Bu siparişe erişim yetkiniz yok.")
            return redirect('orders:order_list')
        return render(request, self.template_name, {'order': order})
```

---

## Template Yapısı

### templates/orders/checkout.html

```
┌──────────────────────────────────────────────────────┐
│  Siparişi Tamamla                                    │
├─────────────────────────┬────────────────────────────┤
│  Teslimat Bilgileri     │  Sipariş Özeti             │
│  ─────────────────      │  ─────────────             │
│  Ad Soyad*  [input]     │  Ürün 1  x2  ₺299.80      │
│  Adres*     [textarea]  │  Ürün 2  x1  ₺49.90       │
│  Şehir*     [input]     │  ─────────────             │
│  Telefon    [input]     │  Toplam: ₺349.70           │
│  Not        [textarea]  │                            │
│                         │  [Siparişi Onayla]         │
└─────────────────────────┴────────────────────────────┘
```

- Form: `method="post"`, CSRF token
- Hata mesajları `{% include 'partials/_messages.html' %}` ile gösterilir
- Sipariş özeti `cart` context değişkeninden gelir

### templates/orders/order_confirm.html

- Başarı alert: Bootstrap `alert-success`
- Sipariş numarası: `#{{ order.id }}`
- Teslimat adresi özeti
- Ürün listesi özeti
- Toplam tutar
- "Siparişlerim" linki → `orders:order_list`
- "Alışverişe Devam" linki → `catalog:home`

### templates/orders/order_list.html

- Tablo: Sipariş No | Tarih | Toplam | Durum Badge | Detay Linki
- Durum badge renkleri:
  - `pending` → `badge bg-warning text-dark`
  - `confirmed` → `badge bg-info`
  - `shipped` → `badge bg-primary`
  - `delivered` → `badge bg-success`
  - `cancelled` → `badge bg-danger`
- Sipariş yoksa: "Henüz sipariş vermediniz." mesajı

### templates/orders/order_detail.html

```
┌──────────────────────────────────────────────────────┐
│  Sipariş #42                    Durum: [Onaylandı]   │
├──────────────────────────────────────────────────────┤
│  Sipariş Tarihi: 07.04.2026                          │
├──────────────────────────────────────────────────────┤
│  Ürünler                                             │
│  ─────────────────────────────────────               │
│  Ürün Adı          Birim Fiyat  Adet  Ara Toplam     │
│  Kahve Fincanı     ₺149.90      x2    ₺299.80        │
│  ─────────────────────────────────────               │
│  Genel Toplam:  ₺349.70                              │
├──────────────────────────────────────────────────────┤
│  Teslimat Adresi                                     │
│  Ali Yılmaz, Örnek Mah. No:5, İstanbul               │
└──────────────────────────────────────────────────────┘
```

---

## Admin Kaydı (apps/orders/admin.py)

```python
from django.contrib import admin
from apps.orders.models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product', 'product_name', 'unit_price', 'quantity', 'line_total']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'status', 'total_price', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['user__email', 'shipping_name']
    readonly_fields = ['total_price', 'created_at', 'updated_at']
    inlines = [OrderItemInline]
    actions = ['mark_confirmed', 'mark_shipped']

    @admin.action(description='Seçili siparişleri Onayla')
    def mark_confirmed(self, request, queryset):
        queryset.update(status='confirmed')

    @admin.action(description='Seçili siparişleri Kargoya Ver')
    def mark_shipped(self, request, queryset):
        queryset.update(status='shipped')
```

---

## Sipariş Akışı (Özet)

```
Sepet → Checkout GET → Checkout POST
                            │
                     CheckoutInputDTO.validate()
                            │
                     OrderService.create_order()
                            │
                    ┌───────┴────────┐
                    │               │
                Stok kontrolü    DB kaydet
                    │               │
                    │          decrement_stock
                    │               │
                    └───────┬────────┘
                            │
                    E-posta gönder (async değil, sync)
                            │
                    CartService.clear_cart()
                            │
                    redirect → order_confirm
```

---

## Sipariş Durum Geçişleri

```
pending → confirmed → shipped → delivered
   │           │
   └──────────→ cancelled
```

Geçersiz geçişler `InvalidOrderStatusTransitionException` fırlatır.
Durum değişikliği sadece admin panelinden veya `OrderAdmin.actions` aracılığıyla yapılır.
