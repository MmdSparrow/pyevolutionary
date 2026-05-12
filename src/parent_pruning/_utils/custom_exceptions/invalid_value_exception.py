from ._base_exception import BaseException


class InvalidValueException(BaseException):
    def __init__(self, logger, value_for_condition="?", variable="?", valid_values="?", input_message=None):
        if input_message is None:
            message = f"Value {value_for_condition} is not valid for the condition with variable {variable}.\nValid values are: {valid_values}"
        else:
            message= input_message
        super(InvalidValueException, self).__init__(message, logger)
