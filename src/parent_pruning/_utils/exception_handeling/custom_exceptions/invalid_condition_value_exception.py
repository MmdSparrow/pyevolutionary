from ._base_exception import BaseException


class InvalidConditionValueException(BaseException):
    def __init__(self, value_for_condition, variable, valid_values, logger=None):
        self.message = f"Value {value_for_condition} is not valid for the condition with variable {variable}.\nValid values are: {valid_values}"
        super(InvalidConditionValueException, self).__init__(self.message, logger)