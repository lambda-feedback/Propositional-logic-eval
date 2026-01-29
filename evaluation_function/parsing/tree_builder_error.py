class BuildError(Exception):
    def __init__(self, message: str, position: int):
        self.message = message
        self.position = position
        super().__init__(f"{message} at position {position}")
