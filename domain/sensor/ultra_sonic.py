from const.config import port_for_ultra_sonic, baudrate, timeout
import serial

from domain.update_data import update_data

coms = serial.Serial(port_for_ultra_sonic, baudrate=baudrate, timeout=timeout)


def ultra_sonic():
    while True:
        clear_serial_buffer()
        data = coms.readline().decode('utf-8').strip()

        if data != "":
            data = int(data)
        else:
            continue

        _, _, _, _, _, _, mask = update_data()

        if data <= 30:
            if mask:
                coms.writelines(b'1')
            else:
                coms.writelines(b'0')


def clear_serial_buffer():
    while coms.in_waiting > 0:
        _ = coms.readline()
