import uuid
from RPi import GPIO
from ..models.event import EventHook
from ..models.pump import Pump

class Thermostat:
    def __init__(self, input_pin, name):

        if input_pin < 0 or input_pin > 40:
            raise Exception("Invalid input pin {}. Must be between 0 and 40".format(input_pin))

        self.__input_pin = input_pin
        self.__name = name

        GPIO.setup(input_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(input_pin, GPIO.BOTH, callback=self.__pin_value_changed, bouncetime=200)

        self.__status = GPIO.input(input_pin)
        self.__on_changed = EventHook()
        self.__uuid = uuid.uuid4()
        self.__controlledPumps = {}

    def __pin_value_changed(self, channel):
        self.__status = GPIO.input(self.__input_pin)
        self.__on_changed.fire(self)

    def add_on_changed(self, on_changed):
        self.__on_changed += on_changed

    def remove_on_changed(self, on_changed):
        self.__on_changed -= on_changed

    def get_status(self):
        return self.__status

    def is_on(self):
        return self.__status == True

    def get_name(self):
        return self.__name

    def get_id(self):
        return self.__uuid

    def get_controlled_pumps(self):
        return self.__controlledPumps

    def add_controlled_pump(self, pump):
        self.__controlledPumps[pump.get_id()] = pump

    def remove_controlled_pump(self, pump):
        del self.__controlledPumps[pump.get_id()]

    def to_json(self):
        controlledPumps = []
        for key in self.__controlledPumps:
            controlledPumps.append(self.__controlledPumps[key].to_json())

        return {
            "id": str(self.__uuid),
            "name": self.__name,
            "isOn": self.is_on(),
            "controlledPumps": controlledPumps
        }