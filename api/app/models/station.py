from RPi import GPIO
from ..models.thermostat import Thermostat
from ..models.pump import Pump

import json

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

        def get_thermostat_from_id(self, id):
            for t in self.__thermostats:
                if t.get_id() == id:
                    return t
            return None

        def get_thermostats(self):
            return self.__thermostats

        def add_pump(self, pin, name):
            self.__pumps.append(Pump(pin, name))

        def get_pumps_count(self):
            return len(self.__pumps)
            
        def get_pump(self, index):
            return self.__pumps[index]

        def get_pump_from_id(self, id):
            for p in self.__pumps:
                if p.get_id() == id:
                    return p
            return None

        def remove_pump(self, pumpId):
            pump = self.get_pump_from_id(pumpId)
            if pump != None:
                for t in self.__thermostats:
                    t.remove_controlled_pump(pump)
                self.__pumps.remove(pump)
                return True
            return False

        def get_pumps(self):
            return self.__pumps

        def save_configuration(self):

            thermostats = []
            for t in self.__thermostats:
                thermostats.append(t.to_json())

            pumps = []
            for p in self.__pumps:
                pumps.append(p.to_json())

            configuration = {
                "thermostats": thermostats,
                "pumps": pumps
            }

            with open("/home/pi/Desktop/station_config.json", "w") as configuration_file:
                json.dump(configuration, configuration_file)

        def read_configuration(self):
            self.__pumps.clear()
            self.__thermostats.clear()

            station = Station()

            with open("/home/pi/Desktop/station_config.json", "r") as configuration_file:
                configuration = json.load(configuration_file)

                for p in configuration["pumps"]:
                    self.__pumps.append(Pump.from_json(p, station))

                for t in configuration["thermostats"]:
                    self.__thermostats.append(Thermostat.from_json(t, station))
            
    __instance = None

    def __new__(cls):
        if not Station.__instance:
            Station.__instance = Station.__Station()
        return Station.__instance

    def __getattr__(self, name):
        return getattr(self.__instance, name)
    
    def __setattr__(self, name):
        return setattr(self.__instance, name)