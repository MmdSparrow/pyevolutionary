from enum import Enum


class TerminationConditionsEnum(Enum):
    PHENOTYPIC_DIVERSITY = "phenotypic diversity"
    FITNESS_LIMIT = "fitness limit"
    ITERATION_NUMBER = "iteration number"
    EVALUATION_NUMBER = "evaluation number"
