from decimal import Decimal

from core.dtos.cart_dtos import CartDTO, CartItemDTO
from core.exceptions.domain_exceptions import OutOfStockException, ProductNotFoundException
from core.repositories.protocols import ProductRepositoryProtocol


class CartService:
    CART_SESSION_KEY = "cart"

    def __init__(
        self,
        product_repo: ProductRepositoryProtocol,
        session: dict,
    ):
        self.product_repo = product_repo
        self.session = session

    def _get_raw_cart(self) -> dict:
        return self.session.get(self.CART_SESSION_KEY, {})

    def _save_cart(self, cart: dict) -> None:
        self.session[self.CART_SESSION_KEY] = cart
        self.session.modified = True

    def get_cart(self) -> CartDTO:
        raw = self._get_raw_cart()
        items = []
        for item in raw.values():
            items.append(
                CartItemDTO(
                    product_id=item["product_id"],
                    name=item["name"],
                    price=Decimal(item["price"]),
                    quantity=item["quantity"],
                    image_url=item.get("image_url"),
                ),
            )
        total = sum(i.price * i.quantity for i in items)
        return CartDTO(
            items=items,
            total_price=total,
            item_count=sum(i.quantity for i in items),
            unique_item_count=len(items),
        )

    def add_item(self, product_id: int, quantity: int = 1) -> CartDTO:
        product = self.product_repo.get_by_id(product_id)
        if not product:
            raise ProductNotFoundException(f"Ürün bulunamadı: id={product_id}")

        cart = self._get_raw_cart()
        key = str(product_id)
        current_qty = cart.get(key, {}).get("quantity", 0)
        new_qty = current_qty + quantity

        if product.stock < new_qty:
            raise OutOfStockException(product.name, product.stock)

        cart[key] = {
            "product_id": product.id,
            "name": product.name,
            "price": str(product.price),
            "quantity": new_qty,
            "image_url": product.image.url if product.image else None,
        }
        self._save_cart(cart)
        return self.get_cart()

    def update_item(self, product_id: int, quantity: int) -> CartDTO:
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
            cart[key]["quantity"] = quantity
            self._save_cart(cart)
        return self.get_cart()

    def remove_item(self, product_id: int) -> CartDTO:
        cart = self._get_raw_cart()
        cart.pop(str(product_id), None)
        self._save_cart(cart)
        return self.get_cart()

    def clear_cart(self) -> None:
        self.session.pop(self.CART_SESSION_KEY, None)
        self.session.modified = True

    def get_item_count(self) -> int:
        raw = self._get_raw_cart()
        return sum(item["quantity"] for item in raw.values())

    def get_total(self) -> Decimal:
        raw = self._get_raw_cart()
        return sum(
            Decimal(item["price"]) * item["quantity"] for item in raw.values()
        )
