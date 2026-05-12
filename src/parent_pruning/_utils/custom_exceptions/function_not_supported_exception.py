from ._base_exception import BaseException


class FunctionNotSupportedException(BaseException):
    def __init__(self, logger, func_name="?", function_objective="?", input_message=None):
        if input_message is None:
            message= (f"{function_objective} function with name {func_name} is not supported!")
        else:
            message= input_message
        super(FunctionNotSupportedException, self).__init__(message, logger)
