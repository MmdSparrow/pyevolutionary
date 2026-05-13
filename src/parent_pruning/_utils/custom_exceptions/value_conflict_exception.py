from ._base_exception import BaseException


class ValueConflictExceptoin(BaseException):
    def __init__(self, logger, input_message):
        super(ValueConflictExceptoin, self).__init__(input_message, logger)
