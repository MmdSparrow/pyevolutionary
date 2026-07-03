import os
import pyevolution._mutation.order_mutation_methods as _order_mutation_module
import pyevolution._crossover.order_crossover_methods as _order_crossover_module

from .__validator import validation
from pyevolution.individuals import OrderIndividual
from pyevolution.optimizers._utils import init_function_by_name
from pyevolution._automation_system import AutomationSystemOrder as _AutomationSystemOrder
from pyevolution.optimizers._base_optimizer._base_optimizer import BaseOptimizer as _BaseOptimizer
from pyevolution._configs.order_optimizer_config import (
    CROSSOVER_PROBABILITY_DEFAULT_VALUE,
    MODE_DEFAULT_VALUE,
    MUTATION_PROBABILITY_DEFAULT_VALUE,
    TERMINATION_CONDITIONS_DEFAULT_VALUE,
    VISUALIZE_DEFAULT_VALUE,
    ANALYZE_DEFAULT_VALUE,
)
from pyevolution._configs.directories import (
    EXTENSION_DIRECTORY_CROSSOVER_METHODS_MODULE,
    EXTENSION_DIRECTORY_MUTATION_METHODS_MODULE,
)
from pyevolution._configs.base_optimizer_config import (
    AVAILABLE_MODES,
    AVAILABLE_TERMINATION_CONDITIONS,
    AVAILABLE_STATISTICS,
)

__all__ = ["OrderOptimizer"]


class OrderOptimizer(_BaseOptimizer, _AutomationSystemOrder):
    def _mutation_func_determiner(self, mutation_method):
        module_path = None
        if self.extension_directory is not None:
            module_path = os.path.join(self.extension_directory, EXTENSION_DIRECTORY_MUTATION_METHODS_MODULE)
        self.mutation_func = init_function_by_name(
            _order_mutation_module,
            module_path,
            mutation_method,
            "mutation",
            self._logger,
        )

    def _crossover_func_determiner(self, crossover_method):
        module_path = None
        if self.extension_directory is not None:
            module_path = os.path.join(self.extension_directory, EXTENSION_DIRECTORY_CROSSOVER_METHODS_MODULE)
        self.crossover_func = init_function_by_name(
            _order_crossover_module,
            module_path,
            crossover_method,
            "crossover",
            self._logger,
        )

    def _generate_note_file(
        self,
        genome_size,
        population_size,
        generation_size,
        parent_selection_method,
        remaining_selection_method,
        crossover_method,
        mutation_method,
        termination_conditions,
        crossover_probability,
        mutation_probability,
        mode,
        pruning_methods,
        pruning_methods_params,
        checkpoint_path=None,
    ):
        self._logger.info("Generate Note File")
        text = f"Genome_size: {genome_size}\
            \nPopulation_size: {population_size}\
            \nGeneration_size: {generation_size}\
            \nParent selection Method: {parent_selection_method}\
            \nRemaining Selection Method: {remaining_selection_method}\
            \nCrossover Method: {crossover_method}\
            \nMutation Method: {mutation_method}\
            \nTermination Conditions: {termination_conditions}\
            \nCrossover Probability: {crossover_probability}\
            \nMutation Probability: {mutation_probability}\
            \nMode: {mode}\
            \nPruning Methods: {pruning_methods}\
            \nPruning Methods Params: {pruning_methods_params}"
        if checkpoint_path:
            text = text + f"\nContinue from checkpoint {checkpoint_path}"
        with open(os.path.join(self.base_directory, "note.txt"), "w") as file_to_write:
            file_to_write.write(text)

    def __init__(
        self,
        evaluation_function,
        show_logs_in_console: bool = True,
        extension_directory: str = None,
    ):
        super().__init__(
            evaluation_function=evaluation_function,
            show_logs_in_console=show_logs_in_console,
            extension_directory=extension_directory,
        )
        # _AutomationSystemOrder.__init__(self, extension_directory)
        # _BaseOptimizer.__init__(
        #     self,
        #     evaluation_function,
        #     show_logs_in_console,
        #     extension_directory,
        # )
        self._logger.info(f"List of available `Order Crossover Methods` functions:{self.AVAILABLE_CROSSOVER_METHODS}")
        self._logger.info(f"List of available `Order Mutation Methods` functions:{self.AVAILABLE_MUTATION_METHODS}")
        self.individual_class = OrderIndividual

    def run(
        self,
        genome_size: int,
        population_size: int,
        generation_size: int,
        parent_selection_method: str,
        remaining_selection_method: str,
        crossover_method: str,
        mutation_method: str,
        termination_conditions: list[str] = TERMINATION_CONDITIONS_DEFAULT_VALUE,
        crossover_probability: float = CROSSOVER_PROBABILITY_DEFAULT_VALUE,
        mutation_probability: float = MUTATION_PROBABILITY_DEFAULT_VALUE,
        mode: str = MODE_DEFAULT_VALUE,
        pruning_methods: list[str] = None,
        pruning_methods_params: list[dict] = None,
        iterations_number: int = None,
        statistics: list[str] = None,
        statistic_sampling_period: int = None,
        evaluation_number: int = None,
        fitness_limit_threshold: float = None,
        phenotypic_diversity_window_size: int = None,
        phenotypic_diversity_error_thereshold: float = None,
        checkpoint_save_period: int = None,
        visualize: bool = VISUALIZE_DEFAULT_VALUE,
        analyze: bool = ANALYZE_DEFAULT_VALUE,
    )-> str:
        validation(
            self._logger,
            self.AVAILABLE_CROSSOVER_METHODS,
            self.AVAILABLE_MUTATION_METHODS,
            crossover_method,
            mutation_method,
        )
        self.crossover_method = crossover_method
        self.mutation_method = mutation_method
        return self._run(
            genome_size,
            population_size,
            generation_size,
            parent_selection_method,
            remaining_selection_method,
            termination_conditions,
            crossover_probability,
            mutation_probability,
            mode,
            pruning_methods,
            pruning_methods_params,
            iterations_number,
            statistics,
            statistic_sampling_period,
            evaluation_number,
            fitness_limit_threshold,
            phenotypic_diversity_window_size,
            phenotypic_diversity_error_thereshold,
            checkpoint_save_period,
            visualize,
            analyze,
        )

    def show_available_crossover_methods(self, return_instead_of_print=False):
        if return_instead_of_print:
            return self.AVAILABLE_CROSSOVER_METHODS
        print("Available Crossover types:")
        print(self.AVAILABLE_CROSSOVER_METHODS)

    def show_available_mutation_methods(self, return_instead_of_print=False):
        if return_instead_of_print:
            return self.AVAILABLE_MUTATION_METHODS
        print("Available Mutation types:")
        print(self.AVAILABLE_MUTATION_METHODS)

    def show_all_availables(self):
        print("Available Termination Conditions:")
        print(AVAILABLE_TERMINATION_CONDITIONS)
        print()

        print("Available Plot Types:")
        print(AVAILABLE_STATISTICS)
        print()

        print("Available Modes:")
        print(AVAILABLE_MODES)
        print()

        print("Available Thereshold Scheduler Methods:")
        print(self.AVAILABLE_SCHEDULER_METHODS)
        print()

        print("Available Parent Selection Methods:")
        print(self.AVAILABLE_PARENT_SELECTION_METHODS)
        print()

        print("Available Remaining Selection Methods:")
        print(self.AVAILABLE_REMAINING_SELECTION_METHODS)
        print()

        print("Available Mutation types:")
        print(self.AVAILABLE_MUTATION_METHODS)
        print()

        print("Available Crossover types:")
        print(self.AVAILABLE_CROSSOVER_METHODS)
