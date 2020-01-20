from RPi import GPIO
from ..models.thermostat import Thermostat
from ..models.pump import Pump

class Station:
    class __Station:
        def __init__(self):
            GPIO.setmode(GPIO.BOARD)
            
            self.__pumps = []
            self.__thermostats = []

        def add_thermostat(self, input_pin, name):
            self.__thermostats.append(Thermostat(input_pin, name))
            
        def get_themostats_count(self):
            return len(self.__thermostats)

        def get_thermostat(self, index):
            return self.__thermostats[index]

        def get_thermostats(self):
            return self.__thermostats

        def add_pump(self, pin, name):
            self.__pumps.append(Pump(pin, name))

        def get_pumps_count(self):
            return len(self.__pumps)
            
        def get_pump(self, index):
            return self.__pumps[index]

        def get_pumps(self):
            return self.__pumps
            
    __instance = None

    def __new__(cls):
        if not Station.__instance:
            Station.__instance = Station.__Station()
        return Station.__instance

    def __getattr__(self, name):
        return getattr(self.__instance, name)
    
    def __setattr__(self, name):
        return setattr(self.__instance, name)