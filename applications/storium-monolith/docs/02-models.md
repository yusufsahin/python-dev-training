# 02 — Model Katmanı

## Genel Kurallar
- Tüm modeller `apps/<domain>/models.py` içinde tanımlanır
- Her model `django.db.models.Model`'den türer
- `__str__` metodu zorunlu
- `created_at` için `auto_now_add=True`, `updated_at` için `auto_now=True`
- Soft delete bu versiyonda uygulanmaz
- `SlugField` alanları admin panelinde `prepopulated_fields` ile otomatik doldurulur

---

## Category (apps/catalog/models.py)

Hiyerarşik kategori yapısı. `parent=None` olan kayıtlar kök kategorilerdir.

| Alan        | Tip                      | Kısıt / Not                                                  |
|-------------|--------------------------|--------------------------------------------------------------|
| id          | AutoField (PK)           | Otomatik                                                     |
| name        | CharField(100)           | blank=False                                                  |
| slug        | SlugField(120)           | unique=True                                                  |
| parent      | ForeignKey('self')       | null=True, blank=True, on_delete=SET_NULL, related_name='children' |
| description | TextField                | blank=True                                                   |
| is_active   | BooleanField             | default=True                                                 |
| created_at  | DateTimeField            | auto_now_add=True                                            |

**Meta**: `ordering = ['name']`, `verbose_name_plural = "categories"`

**Metodlar**:
```python
def __str__(self):
    return self.name

@property
def is_root(self) -> bool:
    return self.parent is None

def get_ancestors(self) -> list['Category']:
    """Kök'e kadar üst kategoriler listesi — breadcrumb için."""
    ancestors = []
    current = self.parent
    while current is not None:
        ancestors.insert(0, current)
        current = current.parent
    return ancestors
```

---

## Product (apps/catalog/models.py)

| Alan        | Tip                      | Kısıt / Not                                                  |
|-------------|--------------------------|--------------------------------------------------------------|
| id          | AutoField (PK)           | Otomatik                                                     |
| category    | ForeignKey(Category)     | on_delete=PROTECT, related_name='products'                   |
| name        | CharField(255)           | blank=False                                                  |
| slug        | SlugField(255)           | unique=True                                                  |
| description | TextField                | blank=True                                                   |
| price       | DecimalField(10,2)       | validators=[MinValueValidator(Decimal('0.01'))]              |
| stock       | PositiveIntegerField     | default=0                                                    |
| image       | ImageField               | upload_to='products/', blank=True, null=True                 |
| is_active   | BooleanField             | default=True                                                 |
| created_at  | DateTimeField            | auto_now_add=True                                            |
| updated_at  | DateTimeField            | auto_now=True                                                |

**Meta**: `ordering = ['-created_at']`

**Metodlar**:
```python
def __str__(self):
    return self.name

@property
def is_in_stock(self) -> bool:
    return self.stock > 0

@property
def display_price(self) -> str:
    """'₺149,90' biçiminde formatlı fiyat döner."""
    return f"₺{self.price:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
```

---

## Order (apps/orders/models.py)

| Alan             | Tip                       | Kısıt / Not                                          |
|------------------|---------------------------|------------------------------------------------------|
| id               | AutoField (PK)            | Otomatik                                             |
| user             | ForeignKey(AUTH_USER_MODEL) | on_delete=PROTECT, related_name='orders'           |
| status           | CharField(20)             | choices=OrderStatus, default='pending'               |
| total_price      | DecimalField(10,2)        | Sipariş anındaki toplam (snapshot — sonradan değişmez)|
| shipping_name    | CharField(200)            | Teslimat adı / soyad                                 |
| shipping_address | TextField                 | Teslimat adresi (sokak, bina, daire)                 |
| shipping_city    | CharField(100)            | Şehir                                                |
| shipping_phone   | CharField(20)             | blank=True                                           |
| notes            | TextField                 | blank=True — müşteri notu                            |
| created_at       | DateTimeField             | auto_now_add=True                                    |
| updated_at       | DateTimeField             | auto_now=True                                        |

**OrderStatus (TextChoices)**:
```python
class OrderStatus(models.TextChoices):
    PENDING    = 'pending',    'Beklemede'
    CONFIRMED  = 'confirmed',  'Onaylandı'
    SHIPPED    = 'shipped',    'Kargoya Verildi'
    DELIVERED  = 'delivered',  'Teslim Edildi'
    CANCELLED  = 'cancelled',  'İptal Edildi'
```

**Meta**: `ordering = ['-created_at']`

**Metodlar**:
```python
def __str__(self):
    return f"Sipariş #{self.id} — {self.user} — {self.get_status_display()}"
```

---

## OrderItem (apps/orders/models.py)

Satın alım anındaki ürün fiyatı ve adı **snapshot** olarak saklanır.
Sonradan ürün fiyatı değişse bile sipariş tutarı sabit kalır.

| Alan          | Tip                   | Kısıt / Not                                              |
|---------------|-----------------------|----------------------------------------------------------|
| id            | AutoField (PK)        | Otomatik                                                 |
| order         | ForeignKey(Order)     | on_delete=CASCADE, related_name='items'                  |
| product       | ForeignKey(Product)   | on_delete=PROTECT (ürün silinmesin diye)                 |
| product_name  | CharField(255)        | Snapshot: sipariş anındaki ürün adı                      |
| unit_price    | DecimalField(10,2)    | Snapshot: sipariş anındaki birim fiyat                   |
| quantity      | PositiveIntegerField  | validators=[MinValueValidator(1)]                        |

**Metodlar**:
```python
def __str__(self):
    return f"{self.product_name} x{self.quantity}"

@property
def line_total(self) -> Decimal:
    return self.unit_price * self.quantity
```

---

## Cart — Session Yapısı (Model YOK)

Cart veritabanında **saklanmaz**. Django session mekanizmasını kullanır.

**Session key**: `'cart'`

```python
# request.session['cart'] veri yapısı:
{
    "42": {                         # key = str(product.id)
        "product_id": 42,
        "name": "Kahve Fincanı Seti",
        "price": "149.90",          # Decimal → str (JSON uyumluluğu için)
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

**Önemli notlar**:
- Session değiştiğinde `request.session.modified = True` set edilmeli
- `price` alanı `str` saklanır (JSON serializasyonu için), kullanırken `Decimal(item['price'])` ile dönüştürülür
- Sepet total = `sum(Decimal(item['price']) * item['quantity'] for item in cart.values())`
- `SESSION_COOKIE_AGE` → `settings.py`'de 1209600 (2 hafta) olarak ayarlanabilir

---

## Migration Notları

```bash
# Tüm migration'ları oluştur
python manage.py makemigrations catalog orders

# Uygula
python manage.py migrate

# Admin'de test için örnek veri
python manage.py createsuperuser
```

`Pillow` paketi ImageField için gereklidir (`requirements.txt`'e eklenmeli).
