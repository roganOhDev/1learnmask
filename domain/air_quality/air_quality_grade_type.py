from enum import Enum

from grade_type import GradeType


class AirQualityGradeType(Enum):
    VERY_GOOD: int = 30
    GOOD: int = 80
    MEDIUM: int = 110
    BAD: int = 150
    VERY_BAD: int

    @staticmethod
    def check_grade(value: int) -> GradeType:
        if value <= AirQualityGradeType.VERY_GOOD.value:
            return GradeType.VERY_GOOD
        elif AirQualityGradeType.VERY_GOOD.value < value & value <= AirQualityGradeType.GOOD.value:
            return GradeType.GOOD
        elif AirQualityGradeType.GOOD.value < value & value <= AirQualityGradeType.MEDIUM.value:
            return GradeType.MEDIUM
        elif AirQualityGradeType.MEDIUM.value < value & value <= AirQualityGradeType.BAD.value:
            return GradeType.BAD
        else:
            return GradeType.VERY_BAD
