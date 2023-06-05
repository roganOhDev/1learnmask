from time import sleep

from const.config import port_for_ultra_sonic, baudrate, timeout
import serial

from domain.update_data import update_data

coms = serial.Serial(port_for_ultra_sonic, baudrate=baudrate, timeout=timeout)


def ultra_sonic():
    while True:
        clear_serial_buffer()
        data = coms.readline().decode('utf-8').strip()

        if data != "":
            try:
                data = int(data)
            except:
                continue

        else:
            continue

        _, _, _, _, _, _, mask = update_data()

        if data <= 30:
            if mask:
                coms.write(b'R')
            else:
                coms.write(b'B')

        sleep(0.5)


def clear_serial_buffer():
    while coms.in_waiting > 0:
        _ = coms.readline()
