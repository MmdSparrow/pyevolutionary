import logging
import os
import sys
from datetime import datetime

from pyevolutionary._configs.directories import CHECKPOINT_DIRECTORY_DEFAULT, LOG_DIRECTORY_DEFAULT, RESULT_DIRECTORY_DEFAULT

__all__ = ["Base"]


class Base:
    def __create_folders(self):
        self.output_directory_name = datetime.now().astimezone().strftime("%Y-%m-%d_%H-%M-%S")
        self.base_directory = os.path.join("outputs", self.output_directory_name)

        self.result_directory = os.path.join(self.base_directory, RESULT_DIRECTORY_DEFAULT)
        os.makedirs(self.result_directory, exist_ok=True)

        self.log_directory = os.path.join(self.base_directory, LOG_DIRECTORY_DEFAULT)
        os.makedirs(self.log_directory, exist_ok=True)

        self.checkpoint_directory = os.path.join(self.base_directory, CHECKPOINT_DIRECTORY_DEFAULT)
        os.makedirs(self.checkpoint_directory, exist_ok=True)

    def __init_logger(self):
        self._logger = logging.getLogger("core_logger")
        self._logger.setLevel(logging.INFO)
        handler = logging.FileHandler(os.path.join(self.log_directory, "runtime.log"))
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        self._logger.addHandler(handler)
        if self.verbose:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(formatter)
            self._logger.addHandler(console_handler)

    def __init__(self, verbose, **kwargs):
        self.__create_folders()
        self.verbose = verbose
        self.__init_logger()
        super().__init__(**kwargs)
