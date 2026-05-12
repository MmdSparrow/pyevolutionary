import os
import sys
import logging

from datetime import datetime
from parent_pruning.configs.directories import RESULT_DIRECTORY_DEFAULT, LOG_DIRECTORY_DEFAULT, CHECKPOINT_DIRECTORY_DEFAULT


class Base:
    def __create_folders(self, base_directory):
        if base_directory is None:
            folder_name = datetime.today().strftime("%Y-%m-%d_%H-%M-%S")
            self.base_directory = os.path.join(self.project_name + "-" + "outputs", folder_name)
        else:
            self.base_directory = base_directory

        self.result_directory = os.path.join(self.base_directory, RESULT_DIRECTORY_DEFAULT)
        os.makedirs(self.result_directory, exist_ok=True)

        self.log_directory = os.path.join(self.base_directory, LOG_DIRECTORY_DEFAULT)
        os.makedirs(self.log_directory, exist_ok=True)

        self.checkpoint_directory = os.path.join(self.base_directory, CHECKPOINT_DIRECTORY_DEFAULT)
        os.makedirs(self.checkpoint_directory, exist_ok=True)

    def __init_logger(self, debug_mode):
        self._logger = logging.getLogger("core_logger")
        self._logger.setLevel(logging.INFO)
        handler = logging.FileHandler(os.path.join(self.log_directory, "runtime.log"))
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        self._logger.addHandler(handler)
        if debug_mode:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(formatter)
            self._logger.addHandler(console_handler)

    def __init__(self, project_name, base_directory, debug_mode):
        self.project_name = project_name
        self.__create_folders(base_directory)
        self.__init_logger(debug_mode)
