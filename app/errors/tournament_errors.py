from typing import Optional


class TournamentDoesNotExistsError(Exception):
    def __init__(self, message: Optional[str] = None) -> None:
        if message is None:
            message = "Tournament does not exist."
        super().__init__(message)


class TournamentNoSlotsError(Exception):
    def __init__(self, message: Optional[str] = None) -> None:
        if message is None:
            message = "Tournament has no slots."
        super().__init__(message)
