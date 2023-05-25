from enum import Enum

from grade_type import GradeType


class FineAirQualityGradeType(Enum):
    VERY_GOOD: int = 15
    GOOD: int = 35
    MEDIUM: int = 55
    BAD: int = 75
    VERY_BAD: int

    @staticmethod
    def check_grade(value: int) -> GradeType:
        if value <= FineAirQualityGradeType.VERY_GOOD.value:
            return GradeType.VERY_GOOD
        elif FineAirQualityGradeType.VERY_GOOD.value < value & value <= FineAirQualityGradeType.GOOD.value:
            return GradeType.GOOD
        elif FineAirQualityGradeType.GOOD.value < value & value <= FineAirQualityGradeType.MEDIUM.value:
            return GradeType.MEDIUM
        elif FineAirQualityGradeType.MEDIUM.value < value & value <= FineAirQualityGradeType.BAD.value:
            return GradeType.BAD
        else:
            return GradeType.VERY_BAD