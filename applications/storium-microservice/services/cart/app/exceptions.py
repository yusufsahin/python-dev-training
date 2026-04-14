class StoriumBaseException(Exception):
    pass


class ProductNotFoundException(StoriumBaseException):
    pass


class OutOfStockException(StoriumBaseException):
    def __init__(self, product_name: str, available: int):
        self.product_name = product_name
        self.available = available
        super().__init__(
            f"'{product_name}' için yeterli stok yok. Mevcut stok: {available}",
        )
