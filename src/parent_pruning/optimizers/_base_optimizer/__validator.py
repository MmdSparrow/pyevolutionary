from parent_pruning._validations import is_presented, is_bigger, is_probability
from parent_pruning._utils.custom_exceptions import InvalidValueError, FunctionNotSupportedError, ValueCantBeNoneError, ValueConflictError
from parent_pruning._configs.base_optimizer_config import (
    AVAILABLE_MODES,
    AVAILABLE_TERMINATION_CONDITIONS,
    AVAILABLE_STATISTICS,
)


def validation(
    logger,
    AVAILABLE_PARENT_SELECTION_METHODS,
    AVAILABLE_REMAINING_SELECTION_METHODS,
    AVAILABLE_PRUNING_METHODS,
    #########################
    project_name,
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
    iterations_number,
    statistics,
    statistic_sampling_period,
    evaluation_number,
    phenotypic_diversity_window_size,
    phenotypic_diversity_error_thereshold,
    checkpoint_save_period,
):
    if not is_presented(project_name):
        raise ValueCantBeNoneError(logger, "project name")
    if not is_presented(genome_size):
        raise ValueCantBeNoneError(logger, input_message="genome size")
    if not is_bigger(genome_size, 1, is_required=True):
        raise InvalidValueError(logger, input_message="genome size must be bigger than 1")
    if not is_presented(population_size):
        raise ValueCantBeNoneError(logger, input_message="genome size")
    if not is_bigger(population_size, 2, is_required=True):
        raise InvalidValueError(logger, input_message="population size must be bigger than 1")
    if not is_presented(generation_size):
        raise ValueCantBeNoneError(logger, input_message="generation size")
    if not is_bigger(generation_size, 0, is_required=True):
        raise InvalidValueError(logger, input_message="generation size must be bigger than 0")
    if parent_selection_method.split("#")[0] not in AVAILABLE_PARENT_SELECTION_METHODS:
        raise FunctionNotSupportedError(logger, parent_selection_method, "parent selection")
    if remaining_selection_method.split("#")[0] not in AVAILABLE_REMAINING_SELECTION_METHODS:
        raise FunctionNotSupportedError(logger, remaining_selection_method, "remaining selection")
    for termination_condition in termination_conditions:
        if termination_condition not in AVAILABLE_TERMINATION_CONDITIONS:
            raise InvalidValueError(logger, termination_condition, "termination condition", AVAILABLE_TERMINATION_CONDITIONS)
    if not is_probability(crossover_probability):
        raise InvalidValueError(logger, input_message="Crossover probabilty must be between 0 and 1")
    if not is_probability(mutation_probability):
        raise InvalidValueError(logger, input_message="Mutation probabilty must be between 0 and 1")
    if mode not in AVAILABLE_MODES:
        raise InvalidValueError(logger, mode, "mode", AVAILABLE_MODES)
    for pruning_method in pruning_methods:
        if pruning_method not in AVAILABLE_PRUNING_METHODS:
            raise FunctionNotSupportedError(logger, pruning_method, "pruning")
    if not is_bigger(iterations_number, 0):
        raise InvalidValueError(logger, input_message="Iteration number must be bigger than 0")
    if statistics is not None:
        for statistic in statistics:
            if statistic not in AVAILABLE_STATISTICS:
                raise InvalidValueError(logger, statistic, "statistic", AVAILABLE_STATISTICS)
    if not is_bigger(statistic_sampling_period):
        raise InvalidValueError(logger, "Statistic sampling period must be bigger than 0")
    if statistics is not None and len(statistics) != 0:
        if statistic_sampling_period is None:
            raise ValueConflictError(logger, input_message="Statistics set but its sampling peiord not set")
    if not is_bigger(evaluation_number):
        raise InvalidValueError(logger, input_message="Evaluation number must be bigger than 0")
    if not is_bigger(phenotypic_diversity_window_size):
        raise InvalidValueError(logger, input_message="Phenotypic diversity window size must be bigger than 0")
    if not is_bigger(phenotypic_diversity_error_thereshold):
        raise InvalidValueError(logger, input_message="Phenotypic diversity error thereshold must be bigger than 0")
    if not is_bigger(checkpoint_save_period):
        raise InvalidValueError(logger, input_message="checkpoint save peiord must be bigger than 0")
