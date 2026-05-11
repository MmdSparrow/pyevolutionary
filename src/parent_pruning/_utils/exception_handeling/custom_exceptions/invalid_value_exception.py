from ._base_exception import BaseException


class InvalidValueException(BaseException):
    def __init__(self, value_for_condition, variable, valid_values, logger=None):
        message = f"Value {value_for_condition} is not valid for the condition with variable {variable}.\nValid values are: {valid_values}"
        super(InvalidValueException, self).__init__(message, logger)
