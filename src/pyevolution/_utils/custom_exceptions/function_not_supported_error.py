from ._base_error import BaseError


class FunctionNotSupportedError(BaseError):
    def __init__(self, logger, func_name="?", function_objective="?", input_message=None):
        if input_message is None:
            message= (f"{function_objective} function with name {func_name} is not supported!")
        else:
            message= input_message
        super(FunctionNotSupportedError, self).__init__(logger, message)
