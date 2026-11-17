from pyevolutionary._enums import ModesEnum, StatisticsEnum, TerminationConditionsEnum

__all__ = [
    "ANALYZE_DEFAULT_VALUE",
    "AVAILABLE_MODES",
    "AVAILABLE_STATISTICS",
    "AVAILABLE_TERMINATION_CONDITIONS",
    "CROSSOVER_PROBABILITY_DEFAULT_VALUE",
    "MODE_DEFAULT_VALUE",
    "MUTATION_PROBABILITY_DEFAULT_VALUE",
    "TERMINATION_CONDITIONS_DEFAULT_VALUE",
    "VISUALIZE_DEFAULT_VALUE",
]
AVAILABLE_MODES = [ModesEnum.AGGREGGATE.value, ModesEnum.FORGETFUL.value]
AVAILABLE_TERMINATION_CONDITIONS = [
    TerminationConditionsEnum.PHENOTYPIC_DIVERSITY.value,
    TerminationConditionsEnum.FITNESS_LIMIT.value,
    TerminationConditionsEnum.ITERATION_NUMBER.value,
    TerminationConditionsEnum.EVALUATIONS_NUMBER.value,
]
AVAILABLE_STATISTICS = [StatisticsEnum.AVG_FITNESS.value, StatisticsEnum.BEST_FITNESS.value, StatisticsEnum.VAR_FITNESS.value, StatisticsEnum.PRUNINGS.value]


############################################################################################3
TERMINATION_CONDITIONS_DEFAULT_VALUE = [TerminationConditionsEnum.ITERATION_NUMBER.value]
CROSSOVER_PROBABILITY_DEFAULT_VALUE = 0.8
MUTATION_PROBABILITY_DEFAULT_VALUE = 0.4
MODE_DEFAULT_VALUE = ModesEnum.AGGREGGATE.value
VISUALIZE_DEFAULT_VALUE = False
ANALYZE_DEFAULT_VALUE = False


del ModesEnum, StatisticsEnum, TerminationConditionsEnum
