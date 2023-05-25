from enum import Enum

from grade_type import GradeType


class YellowDustGradeType(Enum):
    VERY_GOOD: int = 199
    GOOD: int = 399
    MEDIUM: int = 599
    BAD: int = 799
    VERY_BAD: int

    @staticmethod
    def check_grade(value: int) -> GradeType:
        if value <= YellowDustGradeType.VERY_GOOD.value:
            return GradeType.VERY_GOOD
        elif YellowDustGradeType.VERY_GOOD.value < value & value <= YellowDustGradeType.GOOD.value:
            return GradeType.GOOD
        elif YellowDustGradeType.GOOD.value < value & value <= YellowDustGradeType.MEDIUM.value:
            return GradeType.MEDIUM
        elif YellowDustGradeType.MEDIUM.value < value & value <= YellowDustGradeType.BAD.value:
            return GradeType.BAD
        else:
            return GradeType.VERY_BAD
