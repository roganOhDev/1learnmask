from enum import Enum


class AirQualityGradeType(Enum):
    VERY_GOOD: int = 30
    GOOD: int = 80
    MEDIUM: int = 110
    BAD: int = 150
    VERY_BAD: int
