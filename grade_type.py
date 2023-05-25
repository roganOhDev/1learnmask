from enum import Enum


class GradeType(Enum):
    VERY_GOOD: int = 0
    GOOD: int = 3
    MEDIUM: int = 7
    BAD: int = 15
    VERY_BAD: int = 30
