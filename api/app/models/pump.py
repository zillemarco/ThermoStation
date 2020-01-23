from RPi import GPIO
import uuid as UUID

class Pump:
    def __init__(self, pin, name, uuid = None):

        if pin < 0 or pin > 40:
            raise Exception("Invalid input pin {}. Must be between 0 and 40".format(pin))

        self.__pin = pin
        self.__name = name
        self.__uuid = uuid if uuid != None else UUID.uuid4()

    def turn_on(self):
        GPIO.setup(self.__pin, GPIO.OUT)
        GPIO.output(self.__pin, GPIO.LOW)

    def turn_off(self):
        GPIO.setup(self.__pin, GPIO.OUT)
        GPIO.output(self.__pin, GPIO.HIGH)

    def is_on(self):
        GPIO.setup(self.__pin, GPIO.IN)
        return GPIO.input(self.__pin) == GPIO.LOW

    def get_name(self):
        return self.__name

    def get_id(self):
        return self.__uuid

    def to_json(self):
        return {
            "id": str(self.__uuid),
            "name": self.__name,
            "isOn": self.is_on(),
            "pin": self.__pin
        }

    @staticmethod
    def from_json(data, station):
        return Pump(data["pin"], data["name"], UUID.UUID(data["id"]))