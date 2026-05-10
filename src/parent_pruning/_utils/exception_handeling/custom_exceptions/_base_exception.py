class BaseException(Exception):
    def __init__(self, message=None, logger=None):
        if message is None:
            self.message = "Unknow exception was happened in `Parent Pruning` library!"
        self.message = message
        if logger:
            logger.error(self.message)
        super(BaseException, self).__init__(f"{self.message}")
