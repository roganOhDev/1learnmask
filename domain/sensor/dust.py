from const import data_cache
from const.config import port_for_dust, baudrate, timeout
import serial

coms = serial.Serial(port_for_dust, baudrate=baudrate, timeout=timeout)


def get_dust_data_job():
    data_cache.dust_sensor_value = int(float(coms.readline().decode('utf-8').strip()))
