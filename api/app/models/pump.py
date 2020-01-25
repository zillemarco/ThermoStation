from RPi import GPIO
import uuid as UUID
from threading import Timer
import datetime
import traceback
from ..models.db import DB

class Pump:
    def __init__(self, pin, name, stopHour = None, stopMinute = None, startHour = None, startMinute = None, uuid = None):

        if pin < 0 or pin > 40:
            raise Exception("Invalid input pin {}. Must be between 0 and 40".format(pin))

        self.__pin = pin
        self.__name = name
        self.__uuid = uuid if uuid != None else UUID.uuid4()
        self.__shouldBeOn = False

        self.__stopHour = stopHour if stopHour != None else 12
        self.__stopMinute = stopMinute if stopMinute != None else 0
        self.__startHour = startHour if startHour != None else 12
        self.__startMinute = startMinute if startMinute != None else 0

        GPIO.setup(self.__pin, GPIO.OUT)
        GPIO.output(self.__pin, GPIO.HIGH)

        Timer(10, self.__check_time_of_operation).start()

    def __check_time_of_operation(self):
        if not self.__can_be_on():
            GPIO.output(self.__pin, GPIO.HIGH)
        elif self.__shouldBeOn:
            self.turn_on()

        db = DB()
        db.write_data(str(self.get_id()), "on", 1 if self.is_on() else 0)

        Timer(10, self.__check_time_of_operation).start()

    def __can_be_on(self):
        if self.__stopHour != None and self.__stopMinute != None and self.__startHour != None and self.__startMinute != None:
            now = datetime.datetime.now()
            return (now.hour < self.__stopHour or (now.hour == self.__stopHour and now.minute < self.__stopMinute)) or (now.hour > self.__startHour or (now.hour == self.__startHour and now.minute > self.__startMinute))
        else:
            return True

    def turn_on(self):
        self.__shouldBeOn = True
        if self.__can_be_on():
            GPIO.output(self.__pin, GPIO.LOW)

    def turn_off(self):
        self.__shouldBeOn = False
        GPIO.output(self.__pin, GPIO.HIGH)

    def is_on(self):
        return GPIO.input(self.__pin) == GPIO.LOW

    def set_pin(self, pin):
        self.__pin = pin
        GPIO.setup(self.__pin, GPIO.OUT)

    def set_name(self, name):
        self.__name = name

    def get_name(self):
        return self.__name

    def get_id(self):
        return self.__uuid

    def change_start_and_stop_time(self, stopHour, stopMinute, startHour, startMinute):
        self.__stopHour = stopHour
        self.__stopMinute = stopMinute
        self.__startHour = startHour
        self.__startMinute = startMinute

        if not self.__can_be_on():
            self.turn_off()
        elif self.__shouldBeOn:
            self.turn_on()

    def to_json(self):
        return {
            "id": str(self.__uuid),
            "name": self.__name,
            "isOn": self.is_on(),
            "pin": self.__pin,
            "stopHour": self.__stopHour,
            "stopMinute": self.__stopMinute,
            "startHour": self.__startHour,
            "startMinute": self.__startMinute
        }

    @staticmethod
    def from_json(data, station):
        return Pump(data["pin"], data["name"], data["stopHour"], data["stopMinute"], data["startHour"], data["startMinute"], UUID.UUID(data["id"]))