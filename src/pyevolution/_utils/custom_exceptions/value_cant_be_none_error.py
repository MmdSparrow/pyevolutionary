from ._base_error import BaseError


class ValueCantBeNoneError(BaseError):
    def __init__(self, logger, variable="?", input_message=None):
        if input_message is None:
            message = f"Variable {variable} can't be None"
        else:
            message= input_message
        super().__init__(logger, message)
