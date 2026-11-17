from __future__ import annotations

import os
from typing import Final

import pyevolutionary._pruning.pruning_methods as pruning_methods_module
import pyevolutionary._selection_methods.parent_selection as parent_selection_module
import pyevolutionary._selection_methods.remaining_selection as remaining_selection_module
import pyevolutionary._thereshold_scheduler.thereshold_scheduler_methods as thereshold_scheduler_module
from pyevolutionary._configs.directories import (
    EXTENSION_DIRECTORY_CROSSOVER_METHODS_MODULE,
    EXTENSION_DIRECTORY_MUTATION_METHODS_MODULE,
    EXTENSION_DIRECTORY_PARENT_SELECTION_METHODS_MODULE,
    EXTENSION_DIRECTORY_PRUNING_METHODS_MODULE,
    EXTENSION_DIRECTORY_REMAINING_SELECTION_METHODS_MODULE,
    EXTENSION_DIRECTORY_SCHEDULER_METHODS_MODULE,
)

from .__utils import get_non_private_functions_from_module_path, get_non_private_functions_in_module

__all__ = ["AutomationSystem"]


class AutomationSystem:
    def __init__(self, crossover_module, mutation_module, extension_directory=None, **kwargs):
        self.extension_directory = extension_directory
        if extension_directory is None:
            self.AVAILABLE_SCHEDULER_METHODS: Final[list[str]] = get_non_private_functions_in_module(thereshold_scheduler_module)
            self.AVAILABLE_PARENT_SELECTION_METHODS: Final[list[str]] = get_non_private_functions_in_module(parent_selection_module)
            self.AVAILABLE_REMAINING_SELECTION_METHODS: Final[list[str]] = get_non_private_functions_in_module(remaining_selection_module)
            self.AVAILABLE_PRUNING_METHODS: Final[list[str]] = get_non_private_functions_in_module(pruning_methods_module)
            self.AVAILABLE_CROSSOVER_METHODS: Final[list[str]] = get_non_private_functions_in_module(crossover_module)
            self.AVAILABLE_MUTATION_METHODS: Final[list[str]] = get_non_private_functions_in_module(mutation_module)
        else:
            self.AVAILABLE_SCHEDULER_METHODS: Final[list[str]] = get_non_private_functions_in_module(
                thereshold_scheduler_module
            ) + get_non_private_functions_from_module_path(
                os.path.join(extension_directory, EXTENSION_DIRECTORY_SCHEDULER_METHODS_MODULE), add_prefix="extension_directory_"
            )
            self.AVAILABLE_PARENT_SELECTION_METHODS: Final[list[str]] = get_non_private_functions_in_module(
                parent_selection_module
            ) + get_non_private_functions_from_module_path(
                os.path.join(extension_directory, EXTENSION_DIRECTORY_PARENT_SELECTION_METHODS_MODULE), add_prefix="extension_directory_"
            )
            self.AVAILABLE_REMAINING_SELECTION_METHODS: Final[list[str]] = get_non_private_functions_in_module(
                remaining_selection_module
            ) + get_non_private_functions_from_module_path(
                os.path.join(extension_directory, EXTENSION_DIRECTORY_REMAINING_SELECTION_METHODS_MODULE), add_prefix="extension_directory_"
            )
            self.AVAILABLE_PRUNING_METHODS: Final[list[str]] = get_non_private_functions_in_module(
                pruning_methods_module
            ) + get_non_private_functions_from_module_path(
                os.path.join(extension_directory, EXTENSION_DIRECTORY_PRUNING_METHODS_MODULE), add_prefix="extension_directory_"
            )
            self.AVAILABLE_CROSSOVER_METHODS: Final[list[str]] = get_non_private_functions_in_module(
                crossover_module
            ) + get_non_private_functions_from_module_path(
                os.path.join(extension_directory, EXTENSION_DIRECTORY_CROSSOVER_METHODS_MODULE), add_prefix="extension_directory_"
            )
            self.AVAILABLE_MUTATION_METHODS: Final[list[str]] = get_non_private_functions_in_module(
                mutation_module
            ) + get_non_private_functions_from_module_path(
                os.path.join(extension_directory, EXTENSION_DIRECTORY_MUTATION_METHODS_MODULE), add_prefix="extension_directory_"
            )
        super().__init__(**kwargs)
