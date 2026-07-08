import pyevolution._mutation.order_multi_row_mutation_methods as _order_multi_row_mutation_module
import pyevolution._crossover.order_multi_row_crossover_methods as _order_multi_row_crossover_module

from pyevolution.individuals import OrderMultiRowIndividual
from pyevolution.optimizers._base_optimizer._base_optimizer import BaseOptimizer as _BaseOptimizer

from pyevolution._configs.order_multi_row_optimizer_config import (
    CROSSOVER_PROBABILITY_DEFAULT_VALUE,
    MODE_DEFAULT_VALUE,
    MUTATION_PROBABILITY_DEFAULT_VALUE,
    TERMINATION_CONDITIONS_DEFAULT_VALUE,
    VISUALIZE_DEFAULT_VALUE,
    ANALYZE_DEFAULT_VALUE,
)

__all__ = ["OrderMultiRowOptimizer"]


class OrderMultiRowOptimizer(_BaseOptimizer):
    def __init__(
        self,
        evaluation_function,
        show_logs_in_console: bool = True,
        extension_directory: str = None,
    ):
        super().__init__(
            crossover_module=_order_multi_row_crossover_module,
            mutation_module=_order_multi_row_mutation_module,
            evaluation_function=evaluation_function,
            show_logs_in_console=show_logs_in_console,
            extension_directory=extension_directory,
        )

        self.individual_class = OrderMultiRowIndividual

    def run(
        self,
        genome_length: list[int],
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
    ) -> str:
        return self._run(
            genome_length,
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
