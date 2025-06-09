from typing import Optional


class PlayerAlreadyExists(Exception):
    def __init__(self, message: Optional[str] = None) -> None:
        if message is None:
            message = "Player already exists."
        self.message = message
        super().__init__(self.message)
