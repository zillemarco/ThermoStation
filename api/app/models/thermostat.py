import uuid as UUID
from RPi import GPIO
from ..models.event import EventHook
from ..models.pump import Pump
from ..models.db import DB
from threading import Timer

# 
# Tipologia termostato:
#   - 1: classici a muro
#   - 2: digitali
# 

class Thermostat:
    def __init__(self, input_pin, name, tType, targetTemperature, uuid = None, controlledPumps = None):

        if input_pin < 0 or input_pin > 40:
            raise Exception("Invalid input pin {}. Must be between 0 and 40".format(input_pin))

        self.__input_pin = input_pin
        self.__name = name
        self.__type = tType
        self.__targetTemperature = targetTemperature
        self.__currentTemperature = 20

        GPIO.setup(input_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        self.__status = None
        self.__on_changed = EventHook()
        self.__uuid = uuid if uuid != None else UUID.uuid4()
        self.__controlledPumps = controlledPumps if controlledPumps != None else {}

        Timer(1, self.__update_status).start()

    def __update_status(self):

        db = DB()

        if self.__type == 1:
            newStatus = GPIO.input(self.__input_pin) == 0
            db.write_data(str(self.get_id()), "on", 1 if newStatus == True else 0)
            if self.__status == None or newStatus != self.__status:
                self.__status = newStatus
                print("Pin changed status " + str(self.__status))

                for key in self.__controlledPumps:
                    if self.__status:
                        self.__controlledPumps[key].turn_on()
                    else:
                        self.__controlledPumps[key].turn_off()
        else:
            with open("/home/pi/Desktop/termo.txt", "r") as f:
                self.__currentTemperature = float(f.readline())

            newStatus = self.__currentTemperature < self.__targetTemperature

            db.write_data(str(self.get_id()), "temperature", self.__currentTemperature)
            db.write_data(str(self.get_id()), "on", 1 if newStatus == True else 0)
            if self.__status == None or newStatus != self.__status:
                self.__status = newStatus
                print("Pin changed status " + str(self.__status))

                for key in self.__controlledPumps:
                    if self.__status:
                        self.__controlledPumps[key].turn_on()
                    else:
                        self.__controlledPumps[key].turn_off()

        Timer(3, self.__update_status).start()

    def clear_events(self):
        GPIO.remove_event_detect(self.__input_pin)

    def __turn_on_pumps_on_start(self):
        for key in self.__controlledPumps:
            self.__controlledPumps[key].turn_on()
        self.__startTimer.cancel()

    def add_on_changed(self, on_changed):
        self.__on_changed += on_changed

    def remove_on_changed(self, on_changed):
        self.__on_changed -= on_changed

    def get_status(self):
        return {
            "isOn": self.__status == True,
            "currentTemperature": self.__currentTemperature
        }

    def set_pin(self, pin):
        if(pin == self.__input_pin):
            return

        self.__input_pin = pin
        GPIO.setup(self.__input_pin, GPIO.IN)

    def is_on(self):
        return self.__status == True

    def get_name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name

    def get_id(self):
        return self.__uuid

    def get_type(self):
        return self.__type

    def set_type(self, tType):
        self.__type = tType

    def set_target_temperature(self, targetTemperature):
        self.__targetTemperature = targetTemperature

    def get_target_temperature(self):
        return self.__targetTemperature

    def get_current_temperature(self):
        return self.__currentTemperature

    def get_controlled_pumps(self):
        return self.__controlledPumps

    def add_controlled_pump(self, pump):
        if pump.get_id() not in self.__controlledPumps:
            if self.__status:
                pump.turn_on()
            else:
                pump.turn_off()

            self.__controlledPumps[pump.get_id()] = pump

    def remove_controlled_pump(self, pump):
        if pump.get_id() in self.__controlledPumps:
            del self.__controlledPumps[pump.get_id()]

    def clear_controlled_pumps(self):
        self.__controlledPumps.clear()

    def to_json(self):
        controlledPumps = []
        for key in self.__controlledPumps:
            controlledPumps.append(str(key))

        return {
            "id": str(self.__uuid),
            "name": self.__name,
            "isOn": self.is_on(),
            "pin": self.__input_pin,
            "currentTemperature": self.__currentTemperature,
            "targetTemperature": self.__targetTemperature,
            "type": self.__type,
            "controlledPumps": controlledPumps
        }

    @staticmethod
    def from_json(data, station):
        controlledPumps = {}
        for cp in data["controlledPumps"]:
            p = station.get_pump_from_id(UUID.UUID(cp))
            if p != None:
                controlledPumps[p.get_id()] = p

        return Thermostat(data["pin"], data["name"], data["type"], data["targetTemperature"], UUID.UUID(data["id"]), controlledPumps)