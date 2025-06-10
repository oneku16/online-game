class TournamentDoesNotExistsError(Exception):
    def __init__(self, message: str | None = None) -> None:
        if message is None:
            message = "Tournament does not exist."
        super().__init__(message)


class TournamentNoSlotsError(Exception):
    def __init__(self, message: str | None = None) -> None:
        if message is None:
            message = "Tournament has no slots."
        super().__init__(message)


class PlayerAlreadyRegisteredError(Exception):
    def __init__(self, message: str | None = None) -> None:
        if message is None:
            message = "Player already exists."
        self.message = message
        super().__init__(self.message)
