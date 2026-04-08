# 04 — Service Katmanı

## Genel Kurallar
- Her domain için bir servis sınıfı (`core/services/`)
- Bağımlılıklar `__init__` üzerinden Protocol tipli olarak enjekte edilir
- Model nesnelerini Output DTO'ya servis içinde dönüştürür (`_to_dto` private metodları); DTO’lar **Pydantic v2** modelleridir (bkz. `docs/05-dto-layer.md`)
- Hata durumunda `core/exceptions/domain_exceptions.py` exception'larını fırlatır
- Birden fazla DB işlemi içeren metodlar `@transaction.atomic` ile sarılır
- Service asla ORM'e doğrudan erişmez; Repository üzerinden gider

---

## Domain Exceptions (core/exceptions/domain_exceptions.py)

```python
class StoriumBaseException(Exception):
    """Tüm domain exception'larının taban sınıfı."""
    pass


class ProductNotFoundException(StoriumBaseException):
    pass


class OutOfStockException(StoriumBaseException):
    def __init__(self, product_name: str, available: int):
        self.product_name = product_name
        self.available = available
        super().__init__(
            f"'{product_name}' için yeterli stok yok. Mevcut stok: {available}"
        )


class CategoryNotFoundException(StoriumBaseException):
    pass


class OrderNotFoundException(StoriumBaseException):
    pass


class InvalidOrderStatusTransitionException(StoriumBaseException):
    def __init__(self, from_status: str, to_status: str):
        super().__init__(
            f"'{from_status}' → '{to_status}' geçişi geçersiz."
        )


class EmptyCartException(StoriumBaseException):
    pass


class OrderAccessDeniedException(StoriumBaseException):
    pass
```

---

## CatalogService (core/services/catalog_service.py)

```python
from django.core.paginator import Paginator
from core.repositories.protocols import CategoryRepositoryProtocol, ProductRepositoryProtocol
from core.dtos.catalog_dtos import (
    CategoryOutputDTO, ProductOutputDTO, BreadcrumbItemDTO,
    CategoryWithProductsDTO, ProductDetailDTO, ProductListDTO
)
from core.exceptions.domain_exceptions import CategoryNotFoundException, ProductNotFoundException


class CatalogService:
    def __init__(
        self,
        category_repo: CategoryRepositoryProtocol,
        product_repo: ProductRepositoryProtocol,
    ):
        self.category_repo = category_repo
        self.product_repo = product_repo

    # ---- Public metodlar ----

    def get_root_categories(self) -> list[CategoryOutputDTO]:
        """Aktif kök kategorilerin listesini döner."""
        categories = self.category_repo.get_root_categories()
        return [self._category_to_dto(c) for c in categories]

    def get_category_with_products(
        self,
        category_slug: str,
        page: int = 1,
        page_size: int = 12,
    ) -> CategoryWithProductsDTO:
        """
        - Slug ile kategori bulur; bulamazsa CategoryNotFoundException
        - Kategoriye ait aktif ürünleri sayfalı döner
        - Breadcrumb verisi dahil
        """
        category = self.category_repo.get_by_slug(category_slug)
        if not category:
            raise CategoryNotFoundException(f"Kategori bulunamadı: {category_slug}")

        product_qs = self.product_repo.get_by_category(category.id)
        paginator = Paginator(product_qs, page_size)
        page_obj = paginator.get_page(page)

        return CategoryWithProductsDTO(
            category=self._category_to_dto(category),
            products=[self._product_to_dto(p) for p in page_obj.object_list],
            breadcrumb=self._build_breadcrumb(category),
            total_count=paginator.count,
            page=page,
            page_size=page_size,
            total_pages=paginator.num_pages,
        )

    def get_product_detail(self, product_slug: str) -> ProductDetailDTO:
        """
        - Slug ile ürün bulur; bulamazsa ProductNotFoundException
        - İlgili kategori ve breadcrumb dahil
        - İlgili ürünler (aynı kategori, ilk 4)
        """
        product = self.product_repo.get_by_slug(product_slug)
        if not product:
            raise ProductNotFoundException(f"Ürün bulunamadı: {product_slug}")

        related_qs = self.product_repo.get_by_category(product.category_id).exclude(pk=product.pk)[:4]

        return ProductDetailDTO(
            product=self._product_to_dto(product),
            breadcrumb=self._build_breadcrumb(product.category),
            related_products=[self._product_to_dto(p) for p in related_qs],
        )

    def search_products(self, query: str, page: int = 1, page_size: int = 12) -> ProductListDTO:
        """Ürün adı veya açıklamasında arama yapar."""
        product_qs = self.product_repo.search(query)
        paginator = Paginator(product_qs, page_size)
        page_obj = paginator.get_page(page)

        return ProductListDTO(
            products=[self._product_to_dto(p) for p in page_obj.object_list],
            total_count=paginator.count,
            page=page,
            total_pages=paginator.num_pages,
        )

    def get_featured_products(self, count: int = 8) -> list[ProductOutputDTO]:
        """Ana sayfa için öne çıkan ürünler (en yeni, stokta olan)."""
        qs = self.product_repo.get_active_products().filter(stock__gt=0)[:count]
        return [self._product_to_dto(p) for p in qs]

    # ---- Private dönüşüm metodları ----

    def _category_to_dto(self, category) -> CategoryOutputDTO:
        return CategoryOutputDTO(
            id=category.id,
            name=category.name,
            slug=category.slug,
            description=category.description,
            is_root=category.is_root,
            parent_id=category.parent_id,
            children_count=category.children.filter(is_active=True).count(),
        )

    def _product_to_dto(self, product) -> ProductOutputDTO:
        return ProductOutputDTO(
            id=product.id,
            name=product.name,
            slug=product.slug,
            price=product.price,
            stock=product.stock,
            is_in_stock=product.is_in_stock,
            description=product.description,
            image_url=product.image.url if product.image else None,
            category_name=product.category.name,
            category_slug=product.category.slug,
        )

    def _build_breadcrumb(self, category) -> list[BreadcrumbItemDTO]:
        from django.urls import reverse
        ancestors = category.get_ancestors()
        breadcrumb = []
        for anc in ancestors:
            breadcrumb.append(BreadcrumbItemDTO(
                name=anc.name,
                slug=anc.slug,
                url=reverse('category_detail', kwargs={'slug': anc.slug}),
            ))
        breadcrumb.append(BreadcrumbItemDTO(
            name=category.name,
            slug=category.slug,
            url=reverse('category_detail', kwargs={'slug': category.slug}),
        ))
        return breadcrumb
```

---

## CartService (core/services/cart_service.py)

```python
from decimal import Decimal
from core.repositories.protocols import ProductRepositoryProtocol
from core.dtos.cart_dtos import CartDTO, CartItemDTO
from core.exceptions.domain_exceptions import ProductNotFoundException, OutOfStockException


class CartService:
    CART_SESSION_KEY = 'cart'

    def __init__(
        self,
        product_repo: ProductRepositoryProtocol,
        session: dict,              # request.session geçilir
    ):
        self.product_repo = product_repo
        self.session = session

    def _get_raw_cart(self) -> dict:
        return self.session.get(self.CART_SESSION_KEY, {})

    def _save_cart(self, cart: dict) -> None:
        self.session[self.CART_SESSION_KEY] = cart
        self.session.modified = True

    def get_cart(self) -> CartDTO:
        """Session'dan sepeti okur, CartDTO döner."""
        raw = self._get_raw_cart()
        items = []
        for item in raw.values():
            items.append(CartItemDTO(
                product_id=item['product_id'],
                name=item['name'],
                price=Decimal(item['price']),
                quantity=item['quantity'],
                image_url=item.get('image_url'),
            ))
        total = sum(i.price * i.quantity for i in items)
        return CartDTO(
            items=items,
            total_price=total,
            item_count=sum(i.quantity for i in items),
            unique_item_count=len(items),
        )

    def add_item(self, product_id: int, quantity: int = 1) -> CartDTO:
        """
        1. Ürünü DB'den kontrol et (ProductNotFoundException)
        2. Yeterli stok var mı kontrol et (OutOfStockException)
        3. Session'a ekle veya mevcut miktarı artır
        """
        product = self.product_repo.get_by_id(product_id)
        if not product:
            raise ProductNotFoundException(f"Ürün bulunamadı: id={product_id}")

        cart = self._get_raw_cart()
        key = str(product_id)
        current_qty = cart.get(key, {}).get('quantity', 0)
        new_qty = current_qty + quantity

        if product.stock < new_qty:
            raise OutOfStockException(product.name, product.stock)

        cart[key] = {
            'product_id': product.id,
            'name': product.name,
            'price': str(product.price),
            'quantity': new_qty,
            'image_url': product.image.url if product.image else None,
        }
        self._save_cart(cart)
        return self.get_cart()

    def update_item(self, product_id: int, quantity: int) -> CartDTO:
        """
        quantity=0 ise remove_item çağırır.
        Stok kontrolü yapar.
        """
        if quantity <= 0:
            return self.remove_item(product_id)

        product = self.product_repo.get_by_id(product_id)
        if not product:
            raise ProductNotFoundException(f"Ürün bulunamadı: id={product_id}")
        if product.stock < quantity:
            raise OutOfStockException(product.name, product.stock)

        cart = self._get_raw_cart()
        key = str(product_id)
        if key in cart:
            cart[key]['quantity'] = quantity
            self._save_cart(cart)
        return self.get_cart()

    def remove_item(self, product_id: int) -> CartDTO:
        """Session'dan ilgili ürünü kaldırır."""
        cart = self._get_raw_cart()
        cart.pop(str(product_id), None)
        self._save_cart(cart)
        return self.get_cart()

    def clear_cart(self) -> None:
        """Sepeti tamamen temizler."""
        self.session.pop(self.CART_SESSION_KEY, None)
        self.session.modified = True

    def get_item_count(self) -> int:
        """Toplam ürün adedi (miktar toplamı)."""
        raw = self._get_raw_cart()
        return sum(item['quantity'] for item in raw.values())

    def get_total(self) -> Decimal:
        """Toplam tutar."""
        raw = self._get_raw_cart()
        return sum(
            Decimal(item['price']) * item['quantity']
            for item in raw.values()
        )
```

---

## OrderService (core/services/order_service.py)

```python
from django.db import transaction
from core.repositories.protocols import OrderRepositoryProtocol, ProductRepositoryProtocol
from core.dtos.cart_dtos import CartDTO
from core.dtos.order_dtos import CheckoutInputDTO, OrderOutputDTO, OrderItemOutputDTO
from core.exceptions.domain_exceptions import (
    EmptyCartException, OutOfStockException,
    OrderNotFoundException, InvalidOrderStatusTransitionException,
    OrderAccessDeniedException,
)


class OrderService:
    # Geçerli durum geçişleri
    VALID_TRANSITIONS = {
        'pending':   ['confirmed', 'cancelled'],
        'confirmed': ['shipped', 'cancelled'],
        'shipped':   ['delivered'],
        'delivered': [],
        'cancelled': [],
    }

    def __init__(
        self,
        order_repo: OrderRepositoryProtocol,
        product_repo: ProductRepositoryProtocol,
        notification_service,         # EmailNotificationService
    ):
        self.order_repo = order_repo
        self.product_repo = product_repo
        self.notification_service = notification_service

    @transaction.atomic
    def create_order(
        self,
        user_id: int,
        cart_dto: CartDTO,
        checkout_input: CheckoutInputDTO,
    ) -> OrderOutputDTO:
        """
        1. Sepet boşsa EmptyCartException
        2. Her ürün için stok kontrolü (OutOfStockException)
        3. Order + OrderItem'ları kaydet
        4. Her ürünün stok'unu azalt (decrement_stock)
        5. E-posta gönder (notification_service.send_order_placed)
        6. OrderOutputDTO döner
        Not: Sepeti temizleme (clear_cart) View katmanında yapılır.
        """
        if not cart_dto.items:
            raise EmptyCartException("Sepet boş, sipariş oluşturulamaz.")

        # Stok kontrolü
        for item in cart_dto.items:
            product = self.product_repo.get_by_id(item.product_id)
            if not product or product.stock < item.quantity:
                raise OutOfStockException(
                    item.name,
                    product.stock if product else 0
                )

        # Sipariş verisi oluştur
        order_data = {
            'user_id': user_id,
            'status': 'pending',
            'total_price': cart_dto.total_price,
            'shipping_name': checkout_input.shipping_name,
            'shipping_address': checkout_input.shipping_address,
            'shipping_city': checkout_input.shipping_city,
            'shipping_phone': checkout_input.shipping_phone,
            'notes': checkout_input.notes,
            'items': [
                {
                    'product_id': item.product_id,
                    'product_name': item.name,
                    'unit_price': item.price,
                    'quantity': item.quantity,
                }
                for item in cart_dto.items
            ]
        }

        order = self.order_repo.create_order(order_data)

        # Stok düş
        for item in cart_dto.items:
            self.product_repo.decrement_stock(item.product_id, item.quantity)

        # E-posta gönder
        order_dto = self._order_to_dto(order)
        self.notification_service.send_order_placed(order_dto)

        return order_dto

    def get_user_orders(self, user_id: int) -> list[OrderOutputDTO]:
        """Kullanıcının tüm siparişlerini yeniden eskiye sıralar."""
        orders = self.order_repo.get_user_orders(user_id)
        return [self._order_to_dto(o) for o in orders]

    def get_order_detail(self, order_id: int, user_id: int) -> OrderOutputDTO:
        """
        - Siparişi bulur (OrderNotFoundException)
        - Siparişin user_id eşleşmiyorsa OrderAccessDeniedException
        """
        order = self.order_repo.get_by_id(order_id)
        if not order:
            raise OrderNotFoundException(f"Sipariş bulunamadı: id={order_id}")
        if order.user_id != user_id:
            raise OrderAccessDeniedException("Bu siparişe erişim yetkiniz yok.")
        return self._order_to_dto(order)

    def update_order_status(self, order_id: int, new_status: str) -> OrderOutputDTO:
        """
        - Geçiş geçerliyse günceller (VALID_TRANSITIONS)
        - Geçersizse InvalidOrderStatusTransitionException
        - E-posta gönder
        Sadece admin/staff tarafından çağrılır.
        """
        order = self.order_repo.get_by_id(order_id)
        if not order:
            raise OrderNotFoundException(f"Sipariş bulunamadı: id={order_id}")

        allowed = self.VALID_TRANSITIONS.get(order.status, [])
        if new_status not in allowed:
            raise InvalidOrderStatusTransitionException(order.status, new_status)

        updated_order = self.order_repo.update_status(order_id, new_status)
        order_dto = self._order_to_dto(updated_order)
        self.notification_service.send_order_status_changed(order_dto)
        return order_dto

    # ---- Private dönüşüm ----

    def _order_to_dto(self, order) -> OrderOutputDTO:
        return OrderOutputDTO(
            id=order.id,
            status=order.status,
            status_display=order.get_status_display(),
            total_price=order.total_price,
            shipping_name=order.shipping_name,
            shipping_address=order.shipping_address,
            shipping_city=order.shipping_city,
            shipping_phone=order.shipping_phone,
            notes=order.notes,
            items=[self._order_item_to_dto(i) for i in order.items.all()],
            created_at=order.created_at.isoformat(),
            updated_at=order.updated_at.isoformat(),
        )

    def _order_item_to_dto(self, item) -> OrderItemOutputDTO:
        return OrderItemOutputDTO(
            product_id=item.product_id,
            product_name=item.product_name,
            unit_price=item.unit_price,
            quantity=item.quantity,
            line_total=item.line_total,
        )
```

---

## Service Bağımlılıkları Özeti

| Service | Bağımlılıklar |
|---------|--------------|
| CatalogService | CategoryRepositoryProtocol, ProductRepositoryProtocol |
| CartService | ProductRepositoryProtocol, session (dict) |
| OrderService | OrderRepositoryProtocol, ProductRepositoryProtocol, EmailNotificationService |
