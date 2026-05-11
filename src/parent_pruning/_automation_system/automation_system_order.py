import os
import parent_pruning.mutation.order_mutation_methods as order_mutation_module
import parent_pruning.crossover.order_crossover_methods as order_crossover_module

from typing import Final, List
from ._automation_system import AutomationSystem
from .__utils import get_non_private_functions_in_module, get_non_private_functions_from_module_path
from parent_pruning.configs.directories import (
    EXTENSION_DIRECTORY_CROSSOVER_METHODS_MODULE,
    EXTENSION_DIRECTORY_MUTATION_METHODS_MODULE,
)


class AutomationSystemOrder(AutomationSystem):
    def __init__(self, extension_directory=None):
        super().__init__(extension_directory)
        if extension_directory is None:
            self.AVAILABLE_CROSSOVER_METHODS: Final[List[str]] = get_non_private_functions_in_module(order_crossover_module)
            self.AVAILABLE_MUTATION_METHODS: Final[List[str]] = get_non_private_functions_in_module(order_mutation_module)
        else:
            self.AVAILABLE_CROSSOVER_METHODS: Final[List[str]] = get_non_private_functions_in_module(
                order_crossover_module
            ) + get_non_private_functions_from_module_path(os.path.join(extension_directory, EXTENSION_DIRECTORY_CROSSOVER_METHODS_MODULE), add_prefix='extension_directory_')
            self.AVAILABLE_MUTATION_METHODS: Final[List[str]] = get_non_private_functions_in_module(
                order_mutation_module
            ) + get_non_private_functions_from_module_path(os.path.join(extension_directory, EXTENSION_DIRECTORY_MUTATION_METHODS_MODULE), add_prefix='extension_directory_')

