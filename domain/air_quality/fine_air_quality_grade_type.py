from enum import Enum


class FineAirQualityGradeType(Enum):
    VERY_GOOD: int = 15
    GOOD: int = 35
    MEDIUM: int = 55
    BAD: int = 75
    VERY_BAD: int
