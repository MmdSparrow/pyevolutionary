from ._base_exception import BaseException


class ConfigurationException(BaseException):
    def __init__(self, value_for_condition, variable, valid_values, logger=None):
        self.message = f"Value {value_for_condition} is not valid for the condition with variable {variable}.\nValid values are: {valid_values}"
        super(ConfigurationException, self).__init__(self.message, logger)
