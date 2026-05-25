import os
import pyevolution._crossover.order_crossover_methods as _order_crossover_module

from typing import Final, List
from .__utils import get_non_private_functions_in_module, get_non_private_functions_from_module_path
from pyevolution._configs.directories import (
    EXTENSION_DIRECTORY_CROSSOVER_METHODS_MODULE,
    EXTENSION_DIRECTORY_MUTATION_METHODS_MODULE,
)

__all__ = ["AutomationSystemOrder"]


class AutomationSystemOrder:
    def __init__(self, extension_directory=None, **kwargs):
        import pyevolution._mutation.order_mutation_methods as _order_mutation_module

        if extension_directory is None:
            self.AVAILABLE_CROSSOVER_METHODS: Final[List[str]] = get_non_private_functions_in_module(_order_crossover_module)
            self.AVAILABLE_MUTATION_METHODS: Final[List[str]] = get_non_private_functions_in_module(_order_mutation_module)
        else:
            self.AVAILABLE_CROSSOVER_METHODS: Final[List[str]] = get_non_private_functions_in_module(
                _order_crossover_module
            ) + get_non_private_functions_from_module_path(
                os.path.join(extension_directory, EXTENSION_DIRECTORY_CROSSOVER_METHODS_MODULE), add_prefix="extension_directory_"
            )
            self.AVAILABLE_MUTATION_METHODS: Final[List[str]] = get_non_private_functions_in_module(
                _order_mutation_module
            ) + get_non_private_functions_from_module_path(
                os.path.join(extension_directory, EXTENSION_DIRECTORY_MUTATION_METHODS_MODULE), add_prefix="extension_directory_"
            )
        del _order_mutation_module
        super().__init__(**kwargs)
