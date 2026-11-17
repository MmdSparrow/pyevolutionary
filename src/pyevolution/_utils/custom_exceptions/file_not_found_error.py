from ._base_error import BaseError


class FileNotExistError(BaseError):
    def __init__(self, logger, file_path="?", input_message=None):
        if input_message is None:
            message= (f"File {file_path} not found")
        else:
            message= input_message
        super().__init__(logger, message)
