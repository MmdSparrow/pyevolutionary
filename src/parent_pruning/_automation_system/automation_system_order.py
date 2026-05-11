import os
import parent_pruning.mutation.order_mutation_methods as order_mutation_module
import parent_pruning.crossover.order_crossover_methods as order_crossover_module

from typing import Final, List
from ._automation_system import AutomationSystem
from .__utils import get_non_private_functions_in_module, get_non_private_functions_from_module_path


class AutomationSystemOrder(AutomationSystem):
    def __init__(self, extension_directory=None):
        if extension_directory is None:
            self.AVAILABLE_CROSSOVER_METHODS: Final[List[str]] = get_non_private_functions_in_module(order_crossover_module)
            self.AVAILABLE_MUTATION_METHODS: Final[List[str]] = get_non_private_functions_in_module(order_mutation_module)
        else:
            self.AVAILABLE_CROSSOVER_METHODS: Final[List[str]] = get_non_private_functions_in_module(
                order_crossover_module
            ) + get_non_private_functions_from_module_path(os.path.join(extension_directory, "crossover_methods.py"))
            self.AVAILABLE_MUTATION_METHODS: Final[List[str]] = get_non_private_functions_in_module(
                order_mutation_module
            ) + get_non_private_functions_from_module_path(os.path.join(extension_directory, "mutation_methods.py"))
