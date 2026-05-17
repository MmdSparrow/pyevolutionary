from ._base_error import BaseError


class ValueConflictError(BaseError):
    def __init__(self, logger, input_message):
        super(ValueConflictError, self).__init__(logger, input_message)
