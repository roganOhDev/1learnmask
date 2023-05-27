from domain.covid import get as get_covid
from domain.air_quality import get as get_air_quality
from domain.yellow_dust import get as get_yellow_dust
from domain.cold import get as get_cold

def get_data():
    covid_data = get_covid.get_30_days_data()
    air_quality_data = get_air_quality.get_2_days_data()

    return covid_data, air_quality_data

def update_data() -> (int, bool):
    grade_sum = 0

    grade_sum += get_covid.get().value

    pm10_grade, pm25_grade = get_air_quality.get()
    grade_sum += pm10_grade
    grade_sum += pm25_grade

    grade_sum += get_yellow_dust.get().value
    grade_sum += get_cold.get().value

    if grade_sum >= 30:
        return grade_sum, True
    else:
        return grade_sum, False
