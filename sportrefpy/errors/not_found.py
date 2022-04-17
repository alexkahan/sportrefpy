class NotFound(Exception):
    pass


class PlayerNotFound(NotFound):
    def __init__(self, message):
        self.message = message
