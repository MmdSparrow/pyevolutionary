from ._base_exception import BaseException


class ValueNotFoundException(BaseException):
    def __init__(self, value, logger=None):
        message = f"Value {value} not found"
        super(ValueNotFoundException, self).__init__(message, logger)
