

class ValidationError(Exception):
    __slots__ = 'errors'

    def __init__(self, errors):
        self.errors = errors


class EntityDoesNotExist(Exception):
    __slots__ = 'errors'

    def __init__(self, errors):
        self.errors = errors
