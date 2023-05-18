from enum import Enum


class Scope(Enum):
    COMMON: int = 199
    SLIGHTLY_BAD: int = 399
    BAD: int = 799
    VERY_BAD: int
