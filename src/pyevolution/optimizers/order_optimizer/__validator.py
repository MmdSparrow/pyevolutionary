from pyevolution._utils.custom_exceptions import InvalidValueError


def validation(
    logger,
    AVAILABLE_CROSSOVER_METHODS,
    AVAILABLE_MUTATION_METHODS,
    crossover_method,
    mutation_method,
):
    if crossover_method not in AVAILABLE_CROSSOVER_METHODS:
        raise InvalidValueError(logger, crossover_method, "crossover_method", AVAILABLE_CROSSOVER_METHODS)
    if mutation_method not in AVAILABLE_MUTATION_METHODS:
        raise InvalidValueError(logger, mutation_method, "mutation_method", AVAILABLE_MUTATION_METHODS)
