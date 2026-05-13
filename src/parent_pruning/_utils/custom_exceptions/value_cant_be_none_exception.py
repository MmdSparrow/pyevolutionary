from ._base_exception import BaseException


class ValueCantBeNoneException(BaseException):
    def __init__(self, logger, variable="?", input_message=None):
        if input_message is None:
            message = f"Variable {variable} can't be None"
        else:
            message= input_message
        super(ValueCantBeNoneException, self).__init__(logger, message)
