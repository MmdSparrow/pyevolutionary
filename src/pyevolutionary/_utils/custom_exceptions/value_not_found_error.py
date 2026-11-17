from ._base_error import BaseError


class ValueNotFoundError(BaseError):
    def __init__(self, logger, value="?", input_message=None):
        if input_message is None:
            message = f"Value {value} not found"
        else:
            message= input_message
        super().__init__(logger, message)
