def __validation(self, parent_selection_type, remaining_selection_type, pruning_methods, termination_conditions, statistics, mode, logger):
    if parent_selection_type.split('#')[0] not in AVAILABLE_PARENT_SELECTION_ALGORITHMS:
        raise Exception('')
    if remaining_selection_type.split('#')[0] not in AVAILABLE_REMAINING_SELECTION_ALGORITHMS:
        raise Exception('')
    if mode not in AVAILABLE_MODES:
        raise Exception('')
    for pruning_method in pruning_methods:
        if pruning_method not in AVAILABLE_PRUNING_METHODS:
            raise Exception('')
    for termination_condition in termination_conditions:
        if termination_condition not in AVAILABLE_TERMINATION_CONDITIONS:
            raise Exception('')
    if statistics is not None:
        for statistic in statistics:
            if statistic not in AVAILABLE_STATISTICS:
                raise Exception('')
    