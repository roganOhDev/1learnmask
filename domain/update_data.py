from domain.covid import get as get_covid
from domain.air_quality import get as get_air_quality
from domain.yellow_dust import get as get_yellow_dust
from domain.cold import get as get_cold
from grade_type import GradeType


def get_data():
    covid_data = get_covid.get_30_days_data()
    air_quality_data = get_air_quality.get_2_days_data()

    return covid_data, air_quality_data


def update_data() -> (int, int, int, int, int, int, bool):
    grade_sum = 0

    covid_grade = get_covid.get().value
    grade_sum += covid_grade

    pm10_grade, pm25_grade = get_air_quality.get()
    grade_sum += pm10_grade
    grade_sum += pm25_grade

    yellow_dust_grade = get_yellow_dust.get().value
    grade_sum += yellow_dust_grade

    cold_grade = get_cold.get().value
    cold_grade = GradeType.BAD.value
    grade_sum += cold_grade

    return covid_grade, pm10_grade, pm25_grade, yellow_dust_grade, cold_grade, grade_sum, grade_sum >= 30
