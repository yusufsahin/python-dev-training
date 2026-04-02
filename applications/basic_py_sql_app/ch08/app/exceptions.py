class AppValidationError(Exception):
    def __init__(self, message: str | list[str]) -> None:
        if isinstance(message, str):
            self.messages = [message]
        else:
            self.messages = list(message)
        super().__init__(self.messages[0] if self.messages else "")
