from ._base_error import BaseError


class InvalidValueError(BaseError):
    def __init__(self, logger, value_for_condition="?", variable="?", valid_values="?", input_message=None):
        if input_message is None:
            message = f"Value {value_for_condition} is not valid for variable {variable} (valid values: {valid_values})"
        else:
            message= input_message
        super().__init__(logger, message)
