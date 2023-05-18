import serial
from time import sleep
import consts

class BTConn():

    def __init__(self, port: str):
        self.serial = serial.Serial(port)

    def get_pressure(self) -> int:
        self.serial.write(b's')
        while not self.serial.in_waiting:
            sleep(1)
        return int.from_bytes(self.serial.read_all(), 'big')
    
    def get_food_left_in_grams(self) -> int:
        pressure = self.get_pressure()
        return (pressure - consts.TARA_WEIGHT) * consts.GRAMS_PER_SENSOR_UNIT

    def rotate_stepper(self, steps_count: int) -> None:
        self.serial.write(steps_count.to_bytes(1, 'big'))
        while not self.serial.in_waiting:
            sleep(1)
        return int.from_bytes(self.serial.read_all(), 'big')

    def is_empty(self) -> bool:
        return self.get_food_left_in_grams() <= consts.GRAMS_PER_SENSOR_UNIT * consts.UNIT_PRECISION