import os
import sys
import logging

from datetime import datetime
from parent_pruning._configs.directories import RESULT_DIRECTORY_DEFAULT, LOG_DIRECTORY_DEFAULT, CHECKPOINT_DIRECTORY_DEFAULT


class Base:
    def __create_folders(self):
        folder_name = datetime.today().strftime("%Y-%m-%d_%H-%M-%S")
        self.base_directory = os.path.join("outputs", folder_name)

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
        if self.show_logs_in_console:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(formatter)
            self._logger.addHandler(console_handler)

    def __init__(self, show_logs_in_console):
        self.__create_folders()
        self.show_logs_in_console= show_logs_in_console
        self.__init_logger()
