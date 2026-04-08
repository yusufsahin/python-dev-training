# 03 — Repository Katmanı

## Amaç
- ORM sorgularını view ve service'ten soyutlar; iş mantığı bu katmanda **YOK**
- Her domain için: `Protocol` (interface) + `DjangoORM` implementasyonu
- Test edilebilirlik: Protocol sayesinde mock/fake repository yazılabilir
- Dosya konumları: `core/repositories/`

---

## BaseRepository (core/repositories/base.py)

Tüm domain repository'leri bu sınıftan türer. Generic[T] ile tip güvenliği sağlar.

```python
from typing import TypeVar, Generic, Optional
from django.db import models as django_models

T = TypeVar('T', bound=django_models.Model)


class BaseRepository(Generic[T]):
    model_class: type[T]

    def get_by_id(self, pk: int) -> Optional[T]:
        try:
            return self.model_class.objects.get(pk=pk)
        except self.model_class.DoesNotExist:
            return None

    def get_all(self) -> django_models.QuerySet[T]:
        return self.model_class.objects.all()

    def save(self, instance: T) -> T:
        instance.save()
        return instance

    def delete(self, instance: T) -> None:
        instance.delete()
```

---

## Protocol Tanımları (core/repositories/protocols.py)

Protocol, Python'un `typing.Protocol`'ü kullanır.
Bu sayede duck-typing ile test'te fake implementasyon kullanılabilir.

```python
from typing import Protocol, Optional
from django.db.models import QuerySet


class CategoryRepositoryProtocol(Protocol):
    def get_by_id(self, pk: int) -> Optional['Category']: ...
    def get_by_slug(self, slug: str) -> Optional['Category']: ...
    def get_root_categories(self) -> QuerySet['Category']: ...
    def get_active_children(self, parent_id: int) -> QuerySet['Category']: ...


class ProductRepositoryProtocol(Protocol):
    def get_by_id(self, pk: int) -> Optional['Product']: ...
    def get_by_slug(self, slug: str) -> Optional['Product']: ...
    def get_by_category(self, category_id: int, active_only: bool = True) -> QuerySet['Product']: ...
    def get_active_products(self) -> QuerySet['Product']: ...
    def search(self, query: str) -> QuerySet['Product']: ...
    def decrement_stock(self, product_id: int, quantity: int) -> None: ...


class OrderRepositoryProtocol(Protocol):
    def get_by_id(self, pk: int) -> Optional['Order']: ...
    def get_user_orders(self, user_id: int) -> QuerySet['Order']: ...
    def create_order(self, order_data: dict) -> 'Order': ...
    def update_status(self, order_id: int, status: str) -> 'Order': ...
```

---

## DjangoCatalogRepository (core/repositories/catalog_repository.py)

### DjangoCategoryRepository

```python
from typing import Optional
from django.db.models import QuerySet
from core.repositories.base import BaseRepository
from modules.catalog.models import Category


class DjangoCategoryRepository(BaseRepository[Category]):
    model_class = Category

    def get_by_slug(self, slug: str) -> Optional[Category]:
        return Category.objects.filter(slug=slug, is_active=True).first()

    def get_root_categories(self) -> QuerySet[Category]:
        return Category.objects.filter(parent=None, is_active=True).order_by('name')

    def get_active_children(self, parent_id: int) -> QuerySet[Category]:
        return Category.objects.filter(parent_id=parent_id, is_active=True).order_by('name')
```

### DjangoProductRepository

```python
from typing import Optional
from django.db.models import QuerySet, Q, F
from core.repositories.base import BaseRepository
from modules.catalog.models import Product


class DjangoProductRepository(BaseRepository[Product]):
    model_class = Product

    def get_by_slug(self, slug: str) -> Optional[Product]:
        return (
            Product.objects
            .select_related('category')
            .filter(slug=slug, is_active=True)
            .first()
        )

    def get_by_category(self, category_id: int, active_only: bool = True) -> QuerySet[Product]:
        qs = Product.objects.filter(category_id=category_id).select_related('category')
        if active_only:
            qs = qs.filter(is_active=True)
        return qs

    def get_active_products(self) -> QuerySet[Product]:
        return Product.objects.filter(is_active=True).select_related('category')

    def search(self, query: str) -> QuerySet[Product]:
        return Product.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query),
            is_active=True
        ).select_related('category')

    def decrement_stock(self, product_id: int, quantity: int) -> None:
        """
        F() expression kullanarak race condition önlenir.
        Negatife düşmemesi için stok kontrol Service katmanında yapılmalı.
        """
        Product.objects.filter(pk=product_id).update(
            stock=F('stock') - quantity
        )
```

---

## DjangoOrderRepository (core/repositories/order_repository.py)

```python
from typing import Optional
from django.db.models import QuerySet
from core.repositories.base import BaseRepository
from modules.orders.models import Order, OrderItem


class DjangoOrderRepository(BaseRepository[Order]):
    model_class = Order

    def get_by_id(self, pk: int) -> Optional[Order]:
        return (
            Order.objects
            .prefetch_related('items__product')
            .filter(pk=pk)
            .first()
        )

    def get_user_orders(self, user_id: int) -> QuerySet[Order]:
        return (
            Order.objects
            .filter(user_id=user_id)
            .prefetch_related('items')
            .order_by('-created_at')
        )

    def create_order(self, order_data: dict) -> Order:
        """
        order_data yapısı:
        {
            'user_id': int,
            'status': str,
            'total_price': Decimal,
            'shipping_name': str,
            'shipping_address': str,
            'shipping_city': str,
            'shipping_phone': str,
            'notes': str,
            'items': [
                {
                    'product_id': int,
                    'product_name': str,
                    'unit_price': Decimal,
                    'quantity': int
                },
                ...
            ]
        }
        """
        items_data = order_data.pop('items')
        order = Order.objects.create(**order_data)
        for item in items_data:
            OrderItem.objects.create(order=order, **item)
        return self.get_by_id(order.pk)  # prefetch_related ile döner

    def update_status(self, order_id: int, status: str) -> Order:
        Order.objects.filter(pk=order_id).update(status=status)
        return self.get_by_id(order_id)
```

---

## Bağımlılık Kuralları

1. Repository'ler sadece kendi domain'inin modellerini import eder
2. Çapraz domain erişimi gerekiyorsa Service katmanı orkestre eder
3. Repository'ler DTO bilmez; her zaman Model nesnesi döner
4. `select_related` / `prefetch_related` sorgu optimizasyonu Repository'de yapılır
5. `F()` expression ile atomik stok güncellemesi zorunlu (race condition önlemek için)

---

## Sayfalama Notu

Sayfalama Repository yerine Service katmanında Django Paginator ile yapılır:

```python
# core/services/catalog_service.py içinde
from django.core.paginator import Paginator

paginator = Paginator(product_qs, page_size)
page_obj = paginator.get_page(page)
products = list(page_obj.object_list)
```
