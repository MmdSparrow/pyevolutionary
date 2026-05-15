import os
import parent_pruning._mutation.order_mutation_methods as _order_mutation_module
import parent_pruning._crossover.order_crossover_methods as _order_crossover_module

from .__validator import validation
from parent_pruning.individuals import OrderIndividual
from parent_pruning.optimizers._utils import init_function_by_name
from parent_pruning._automation_system import AutomationSystemOrder
from parent_pruning.optimizers._base_optimizer.base_optimizer import BaseOptimizer
from parent_pruning._configs.order_optimizer_config import (
    CROSSOVER_PROBABILITY_DEFAULT_VALUE,
    MODE_DEFAULT_VALUE,
    MUTATION_PROBABILITY_DEFAULT_VALUE,
    TERMINATION_CONDITIONS_DEFAULT_VALUE,
    VISUALIZE_DEFAULT_VALUE,
)
from parent_pruning._configs.directories import (
    EXTENSION_DIRECTORY_CROSSOVER_METHODS_MODULE,
    EXTENSION_DIRECTORY_MUTATION_METHODS_MODULE,
)
from parent_pruning._configs.base_optimizer_config import (
    AVAILABLE_MODES,
    AVAILABLE_TERMINATION_CONDITIONS,
    AVAILABLE_STATISTICS,
)


class OrderOptimizer(AutomationSystemOrder, BaseOptimizer):
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
            \nMode: {mode}"
        if checkpoint_path:
            text = text + f"\nContinue from checkpoint {checkpoint_path}"
        with open(os.path.join(self.base_directory, "note.txt"), "w") as file_to_write:
            file_to_write.write(text)

    def __init__(
        self,
        input_data,
        evaluation_function,
        show_logs_in_console: bool = True,
        extension_directory: str = None,
    ):
        AutomationSystemOrder.__init__(self, extension_directory)
        BaseOptimizer.__init__(
            self,
            input_data,
            evaluation_function,
            show_logs_in_console,
            extension_directory,
        )
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
        visualize:bool= False,
        analyze:bool=False,
    ):
        validation(
            self._logger,
            self.AVAILABLE_CROSSOVER_METHODS,
            self.AVAILABLE_MUTATION_METHODS,
            crossover_method,
            mutation_method,
        )
        self.crossover_method = crossover_method
        self.mutation_method = mutation_method
        self._run(
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
