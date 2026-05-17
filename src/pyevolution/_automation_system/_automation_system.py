import os
import pyevolution._pruning.pruning_methods as pruning_methods_module
import pyevolution._selection_methods.parent_selection as parent_selection_module
import pyevolution._selection_methods.remaining_selection as remaining_selection_module
import pyevolution._thereshold_scheduler.thereshold_scheduler_methods as thereshold_scheduler_module

from typing import Final, List
from .__utils import get_non_private_functions_in_module, get_non_private_functions_from_module_path
from pyevolution._configs.directories import (
    EXTENSION_DIRECTORY_PARENT_SELECTION_METHODS_MODULE,
    EXTENSION_DIRECTORY_PRUNING_METHODS_MODULE,
    EXTENSION_DIRECTORY_REMAINING_SELECTION_METHODS_MODULE,
    EXTENSION_DIRECTORY_SCHEDULER_METHODS_MODULE,
)


class AutomationSystem:
    def __init__(self, extension_directory=None):
        self.extension_directory = extension_directory
        if extension_directory is None:
            self.AVAILABLE_SCHEDULER_METHODS: Final[List[str]] = get_non_private_functions_in_module(thereshold_scheduler_module)
            self.AVAILABLE_PARENT_SELECTION_METHODS: Final[List[str]] = get_non_private_functions_in_module(parent_selection_module)
            self.AVAILABLE_REMAINING_SELECTION_METHODS: Final[List[str]] = get_non_private_functions_in_module(remaining_selection_module)
            self.AVAILABLE_PRUNING_METHODS: Final[List[str]] = get_non_private_functions_in_module(pruning_methods_module)
        else:
            self.AVAILABLE_SCHEDULER_METHODS: Final[List[str]] = get_non_private_functions_in_module(
                thereshold_scheduler_module
            ) + get_non_private_functions_from_module_path(os.path.join(extension_directory, EXTENSION_DIRECTORY_SCHEDULER_METHODS_MODULE), add_prefix='extension_directory_')
            self.AVAILABLE_PARENT_SELECTION_METHODS: Final[List[str]] = get_non_private_functions_in_module(
                parent_selection_module
            ) + get_non_private_functions_from_module_path(os.path.join(extension_directory, EXTENSION_DIRECTORY_PARENT_SELECTION_METHODS_MODULE), add_prefix='extension_directory_')
            self.AVAILABLE_REMAINING_SELECTION_METHODS: Final[List[str]] = get_non_private_functions_in_module(
                remaining_selection_module
            ) + get_non_private_functions_from_module_path(os.path.join(extension_directory, EXTENSION_DIRECTORY_REMAINING_SELECTION_METHODS_MODULE), add_prefix='extension_directory_')
            self.AVAILABLE_PRUNING_METHODS: Final[List[str]] = get_non_private_functions_in_module(
                pruning_methods_module
            ) + get_non_private_functions_from_module_path(os.path.join(extension_directory, EXTENSION_DIRECTORY_PRUNING_METHODS_MODULE), add_prefix='extension_directory_')
