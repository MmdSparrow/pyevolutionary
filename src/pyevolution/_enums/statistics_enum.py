from enum import Enum

__all__ = ["StatisticsEnum"]


class StatisticsEnum(Enum):
    AVG_FITNESS = "avg fitness"
    BEST_FITNESS = "best fitness"
    VAR_FITNESS = "var fitness"
    PRUNINGS = "prunings"
