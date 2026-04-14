class StoriumBaseException(Exception):
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


class OutOfStockException(StoriumBaseException):
    pass


class IntegrationError(StoriumBaseException):
    pass
