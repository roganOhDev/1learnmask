from domain.covid import get as get_covid
from domain.air_quality import get as get_air_quality
from domain.yellow_dust import get as get_yellow_dust


def update_data():
    get_covid.get()
    get_air_quality.get()
    get_yellow_dust.get()
