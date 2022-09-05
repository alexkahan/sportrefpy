class PlayerNotFoundError(Exception):
    def __init__(self, name):
        self.name = name
        self.message = f"'{self.name}' not found. Names are case-sensitive."
        super().__init__(self.message)
