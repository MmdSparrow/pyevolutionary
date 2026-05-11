import os
import parent_pruning.pruning.pruning_methods as pruning_methods_module
import parent_pruning.selection_methods.parent_selection as parent_selection_module
import parent_pruning.selection_methods.remaining_selection as remaining_selection_module
import parent_pruning.thereshold_scheduler.thereshold_scheduler_methods as thereshold_scheduler_module


from typing import Final, List
from .__utils import get_non_private_functions_in_module, get_non_private_functions_from_module_path


class AutomationSystem:
    def __init__(self, extension_directory=None):
        if extension_directory is None:
            self.AVAILABLE_SCHEDULER_METHODS: Final[List[str]] = get_non_private_functions_in_module(thereshold_scheduler_module)
            self.AVAILABLE_PARENT_SELECTION_METHODS: Final[List[str]] = get_non_private_functions_in_module(parent_selection_module)
            self.AVAILABLE_REMAINING_SELECTION_METHODS: Final[List[str]] = get_non_private_functions_in_module(remaining_selection_module)
            self.AVAILABLE_PRUNING_METHODS: Final[List[str]] = get_non_private_functions_in_module(pruning_methods_module)
        else:
            self.AVAILABLE_SCHEDULER_METHODS: Final[List[str]] = get_non_private_functions_in_module(
                thereshold_scheduler_module
            ) + get_non_private_functions_from_module_path(os.path.join(extension_directory, "scheduler_methods.py"))
            self.AVAILABLE_PARENT_SELECTION_METHODS: Final[List[str]] = get_non_private_functions_in_module(
                parent_selection_module
            ) + get_non_private_functions_from_module_path(os.path.join(extension_directory, "parent_selection_methods.py"))
            self.AVAILABLE_REMAINING_SELECTION_METHODS: Final[List[str]] = get_non_private_functions_in_module(
                remaining_selection_module
            ) + get_non_private_functions_from_module_path(os.path.join(extension_directory, "remaining_selection_methods.py"))
            self.AVAILABLE_PRUNING_METHODS: Final[List[str]] = get_non_private_functions_in_module(
                pruning_methods_module
            ) + get_non_private_functions_from_module_path(os.path.join(extension_directory, "pruning_methods.py"))
