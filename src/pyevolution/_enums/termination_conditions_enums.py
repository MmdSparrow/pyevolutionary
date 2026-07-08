from enum import Enum

__all__ = ["TerminationConditionsEnum"]


class TerminationConditionsEnum(Enum):
    PHENOTYPIC_DIVERSITY = "phenotypic diversity"
    FITNESS_LIMIT = "fitness limit"
    ITERATION_NUMBER = "iteration number"
    EVALUATIONS_NUMBER = "evaluation number"
