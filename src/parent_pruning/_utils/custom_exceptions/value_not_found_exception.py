from ._base_exception import BaseException


class ValueNotFoundException(BaseException):
    def __init__(self, logger, value="?", input_message=None):
        if input_message is None:
            message = f"Value {value} not found"
        else:
            message= input_message
        super(ValueNotFoundException, self).__init__(message, logger)
