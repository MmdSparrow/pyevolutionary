class BaseError(Exception):
    def __init__(self, logger, message=None):
        if message is None:
            self.message = "Unknow exception was happened in `Parent Pruning` library!"
        self.message = message
        if logger is not None:
            logger.error(self.message)
        super(BaseError, self).__init__(f"{self.message}")
