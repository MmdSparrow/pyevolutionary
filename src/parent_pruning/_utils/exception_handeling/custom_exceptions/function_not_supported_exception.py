from ._base_exception import BaseException


class FunctionNotSupportedException(BaseException):
    def __init__(self, func_name, function_objective, logger=None):
        message= (f"{function_objective} function with name {func_name} is not supported!")
        super(FunctionNotSupportedException, self).__init__(message, logger)
