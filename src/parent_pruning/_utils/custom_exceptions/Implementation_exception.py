from ._base_exception import BaseException


class ImplementationException(BaseException):
    def __init__(self, input_message):
        super(ImplementationException, self).__init__(input_message, None)
