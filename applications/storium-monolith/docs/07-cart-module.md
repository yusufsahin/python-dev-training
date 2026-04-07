# 07 — Cart (Sepet) Modülü

## Kapsam
Cart modülü **veritabanı kullanmaz**. Tüm durum Django session'ında tutulur.
Her request'te `CartService` session üzerinden çalışır.
`apps/cart/` içinde model dosyası oluşturulmaz.

---

## URL Yapısı (apps/cart/urls.py)

```python
from django.urls import path
from apps.cart import views

app_name = 'cart'

urlpatterns = [
    path('sepet/', views.CartDetailView.as_view(), name='cart_detail'),
    path('sepet/ekle/', views.AddToCartView.as_view(), name='cart_add'),
    path('sepet/guncelle/', views.UpdateCartView.as_view(), name='cart_update'),
    path('sepet/sil/<int:product_id>/', views.RemoveFromCartView.as_view(), name='cart_remove'),
    path('sepet/temizle/', views.ClearCartView.as_view(), name='cart_clear'),
]
```

Ana `storium/urls.py`'de:
```python
path('', include('apps.cart.urls', namespace='cart')),
```

---

## Session Veri Yapısı

```python
# request.session['cart'] yapısı:
{
    "42": {                           # key = str(product.id)
        "product_id": 42,
        "name": "Kahve Fincanı Seti",
        "price": "149.90",            # Decimal → str (JSON serializasyonu için)
        "quantity": 2,
        "image_url": "/media/products/kfset.jpg"
    },
    "17": {
        "product_id": 17,
        "name": "Çay Bardağı",
        "price": "49.90",
        "quantity": 1,
        "image_url": "/media/products/bardak.jpg"
    }
}
```

Kurallar:
- Session key her zaman `str(product.id)`
- `price` her zaman `str` saklanır (JSON uyumluluğu)
- `request.session.modified = True` — session değiştiğinde set edilmeli

---

## Views (apps/cart/views.py)

### CartDetailView (GET)

```python
class CartDetailView(View):
    template_name = 'cart/cart_detail.html'

    def get(self, request):
        service = CartService(
            product_repo=DjangoProductRepository(),
            session=request.session
        )
        cart = service.get_cart()
        return render(request, self.template_name, {'cart': cart})
```

### AddToCartView (POST only)

```python
class AddToCartView(View):
    def post(self, request):
        product_id = int(request.POST.get('product_id'))
        quantity = int(request.POST.get('quantity', 1))
        service = CartService(product_repo=DjangoProductRepository(), session=request.session)
        try:
            service.add_item(product_id, quantity)
            messages.success(request, "Ürün sepete eklendi.")
        except ProductNotFoundException:
            messages.error(request, "Ürün bulunamadı.")
        except OutOfStockException as e:
            messages.warning(request, str(e))
        # Ürün detay sayfasına geri dön (varsa)
        next_url = request.POST.get('next') or reverse('cart:cart_detail')
        return redirect(next_url)
```

### UpdateCartView (POST only)

```python
class UpdateCartView(View):
    def post(self, request):
        product_id = int(request.POST.get('product_id'))
        quantity = int(request.POST.get('quantity', 0))
        service = CartService(product_repo=DjangoProductRepository(), session=request.session)
        try:
            service.update_item(product_id, quantity)
            if quantity > 0:
                messages.success(request, "Sepet güncellendi.")
            else:
                messages.info(request, "Ürün sepetten çıkarıldı.")
        except OutOfStockException as e:
            messages.warning(request, str(e))
        return redirect('cart:cart_detail')
```

### RemoveFromCartView (POST only)

```python
class RemoveFromCartView(View):
    def post(self, request, product_id):
        service = CartService(product_repo=DjangoProductRepository(), session=request.session)
        service.remove_item(product_id)
        messages.info(request, "Ürün sepetten çıkarıldı.")
        return redirect('cart:cart_detail')
```

### ClearCartView (POST only)

```python
class ClearCartView(View):
    def post(self, request):
        service = CartService(product_repo=DjangoProductRepository(), session=request.session)
        service.clear_cart()
        messages.info(request, "Sepet temizlendi.")
        return redirect('cart:cart_detail')
```

---

## Context Processor (apps/cart/context_processors.py)

Her template'de `{{ cart_item_count }}` kullanılabilmesi için:

```python
def cart_context(request):
    """Tüm template'lere sepet özet bilgisi ekler."""
    session = getattr(request, 'session', {})
    cart_data = session.get('cart', {})
    item_count = sum(item['quantity'] for item in cart_data.values())
    return {'cart_item_count': item_count}
```

`settings/base.py`'de `TEMPLATES[0]['OPTIONS']['context_processors']` listesine ekle:
```python
'apps.cart.context_processors.cart_context',
```

Navbar'da kullanım:
```html
<a href="{% url 'cart:cart_detail' %}">
  Sepet
  {% if cart_item_count > 0 %}
    <span class="badge bg-danger">{{ cart_item_count }}</span>
  {% endif %}
</a>
```

---

## Sepet Template (templates/cart/cart_detail.html)

```
┌──────────────────────────────────────────────────────┐
│  Sepetiniz (N ürün)                                  │
├──────────────────────────────────────────────────────┤
│  [Görsel] Ürün Adı    Birim Fiyat  [qty input] Ara Toplam  [Sil] │
│  [Görsel] Ürün Adı    Birim Fiyat  [qty input] Ara Toplam  [Sil] │
├──────────────────────────────────────────────────────┤
│              Toplam: ₺XXX.XX                         │
│         [Siparişi Tamamla]  [Alışverişe Devam]       │
└──────────────────────────────────────────────────────┘
```

Template detayları:
- Boş sepet: `{% if not cart.items %}` → "Sepetiniz boş" mesajı + "Alışverişe Başla" butonu
- Her satır için ayrı güncelleme formu (POST `cart_update`):
  ```html
  <form method="post" action="{% url 'cart:cart_update' %}">
    {% csrf_token %}
    <input type="hidden" name="product_id" value="{{ item.product_id }}">
    <input type="number" name="quantity" value="{{ item.quantity }}" min="1" max="99">
    <button type="submit" class="btn btn-sm btn-outline-secondary">Güncelle</button>
  </form>
  ```
- Her satır için ayrı silme formu (POST `cart_remove`):
  ```html
  <form method="post" action="{% url 'cart:cart_remove' product_id=item.product_id %}">
    {% csrf_token %}
    <button type="submit" class="btn btn-sm btn-outline-danger">Sil</button>
  </form>
  ```
- Sağ alt köşede özet kart: Toplam, "Siparişi Tamamla" → `orders:checkout`

---

## Sepet İş Kuralları

1. Giriş yapmamış kullanıcılar da sepet kullanabilir (session tabanlı)
2. Aynı ürün tekrar eklenirse miktarı artırılır (yeni satır açılmaz)
3. Stok aşılırsa `OutOfStockException` fırlatılır → kullanıcıya `messages.warning`
4. Checkout'a geçmek için giriş zorunludur (`@login_required` orders view'ında)
5. Session süresi dolarsa sepet kaybolur (kullanıcı bilgilendirilmez — normal davranış)
6. `SESSION_ENGINE = 'django.contrib.sessions.backends.db'` kullanılır (varsayılan)
