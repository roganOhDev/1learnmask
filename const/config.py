from enum import Enum

# radar graph
angle = 0
label_size = 12
labels = []
while angle < 360:
    labels.append(str(angle) + " degree")
    angle += round(360 / label_size)

max_distance = 25

radar_latency = 0.5
# database
db_name = "test.db"


# version = RunVersion.debug
class RunVersion(Enum):
    debug = "DEBUG"
    demo = "DEMO"


version = RunVersion.demo

# arduino
# port = "COM3"
# port = "/dev/cu.Bluetooth-Incoming-Port"
port = "/dev/cu.usbmodem1101"
baudrate = 9600
timeout = 2
