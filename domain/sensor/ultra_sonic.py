from const iㅇmport data_cache
from const.config import port_for_ultra_sonic, baudrate, timeout
import serial

from domain.update_data import update_data

coms = serial.Serial(port_for_ultra_sonic, baudrate=baudrate, timeout=timeout)


def ultra_sonic():
    while True:
        clear_serial_buffer()

        ultra_sonic_value = int(float(coms.readline().decode('utf-8').strip()))
        _, _, _, _, _, _, _, mask = update_data()

        if ultra_sonic_value <= 30:
            if mask:
                coms.writelines("1")
            else:
                coms.writelines("0")

def clear_serial_buffer():
    while coms.in_waiting > 1:
        _ = coms.readline()
