from parent_pruning._enums.modes_enum import ModesEnum
from parent_pruning._enums.statistics_enum import StatisticsEnum
from parent_pruning._enums.termination_conditions_enums import TerminationConditionsEnum


AVAILABLE_MODES = [ModesEnum.AGGREGGATE, ModesEnum.FORGETFUL]
AVAILABLE_TERMINATION_CONDITIONS = [
    TerminationConditionsEnum.PHENOTYPIC_DIVERSITY,
    TerminationConditionsEnum.GENOTYPIC_DIVERSITY,
    TerminationConditionsEnum.FITNESS_LIMIT,
    TerminationConditionsEnum.ITERATION_NUMBER,
    TerminationConditionsEnum.EVALUATION_NUMBER,
]
AVAILABLE_STATISTICS = [StatisticsEnum.AVG_FITNESS, StatisticsEnum.BEST_FITNESS, StatisticsEnum.VAR_FITNESS, StatisticsEnum.PRUNINGS]


############################################################################################3
TERMINATION_CONDITIONS_DEFAULT_VALUE = [TerminationConditionsEnum.ITERATION_NUMBER]
CROSSOVER_PROBABILITY_DEFAULT_VALUE = 0.8
MUTATION_PROBABILITY_DEFAULT_VALUE = 0.4
MODE_DEFAULT_VALUE = ModesEnum.AGGREGGATE
VISUALIZE_DEFAULT_VALUE = False
