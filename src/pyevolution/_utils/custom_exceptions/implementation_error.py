from ._base_error import BaseError


class ImplementationError(BaseError):
    def __init__(self, input_message):
        super().__init__(None, input_message)
