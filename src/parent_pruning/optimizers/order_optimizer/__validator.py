from parent_pruning.configs.order_optimizer_config import (
    AVAILABLE_CROSSOVER_METHODS,
    AVAILABLE_MUTATION_METHODS,
)


def validation(crossover_type, mutation_type, logger):
    if crossover_type not in AVAILABLE_CROSSOVER_METHODS:
        raise Exception("")
    if mutation_type not in AVAILABLE_MUTATION_METHODS:
        raise Exception("")
