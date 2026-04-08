class StoriumBaseException(Exception):
    """Tüm domain exception'larının taban sınıfı."""


class ProductNotFoundException(StoriumBaseException):
    pass


class OutOfStockException(StoriumBaseException):
    def __init__(self, product_name: str, available: int):
        self.product_name = product_name
        self.available = available
        super().__init__(
            f"'{product_name}' için yeterli stok yok. Mevcut stok: {available}",
        )


class CategoryNotFoundException(StoriumBaseException):
    pass


class OrderNotFoundException(StoriumBaseException):
    pass


class InvalidOrderStatusTransitionException(StoriumBaseException):
    def __init__(self, from_status: str, to_status: str):
        super().__init__(
            f"'{from_status}' → '{to_status}' geçişi geçersiz.",
        )


class EmptyCartException(StoriumBaseException):
    pass


class OrderAccessDeniedException(StoriumBaseException):
    pass
