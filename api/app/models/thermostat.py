import uuid as UUID
from RPi import GPIO
from threading import Timer
from ..models.event import EventHook
from ..models.pump import Pump

class Thermostat:
    def __init__(self, input_pin, name, uuid = None, controlledPumps = None):

        if input_pin < 0 or input_pin > 40:
            raise Exception("Invalid input pin {}. Must be between 0 and 40".format(input_pin))

        self.__input_pin = input_pin
        self.__name = name

        GPIO.setup(input_pin, GPIO.IN)
        GPIO.add_event_detect(input_pin, GPIO.BOTH, callback=self.__pin_value_changed, bouncetime=200)

        self.__status = GPIO.input(input_pin)
        self.__on_changed = EventHook()
        self.__uuid = uuid if uuid != None else UUID.uuid4()
        self.__controlledPumps = controlledPumps if controlledPumps != None else {}

        # Serve a saltare la prima notifica perche' mi arriva il segnale invertito (?)
        # Questo capita solo all'avvio quindi controllo lo stato ed eventualmente
        # attivo le pompe ora, skippando la prima chiamata alla callback che risulterebbe
        # errata
        self.__ignorePinValueChange = True

        if not self.__status:
            for key in self.__controlledPumps:
                self.__controlledPumps[key].turn_on()

    def __turn_on_pumps_on_start(self):
        for key in self.__controlledPumps:
            self.__controlledPumps[key].turn_on()
        self.__startTimer.cancel()

    def __pin_value_changed(self, channel):

        if self.__ignorePinValueChange:
            self.__ignorePinValueChange = False
            return

        self.__status = GPIO.input(self.__input_pin)
        self.__on_changed.fire(self)

        for key in self.__controlledPumps:
            if self.__status:
                self.__controlledPumps[key].turn_on()
            else:
                self.__controlledPumps[key].turn_off()

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
        if pump.get_id() in self.__controlledPumps:
            del self.__controlledPumps[pump.get_id()]

    def to_json(self):
        controlledPumps = []
        for key in self.__controlledPumps:
            controlledPumps.append(self.__controlledPumps[key].to_json())

        return {
            "id": str(self.__uuid),
            "name": self.__name,
            "isOn": self.is_on(),
            "pin": self.__input_pin,
            "controlledPumps": controlledPumps
        }

    @staticmethod
    def from_json(data, station):
        controlledPumps = {}
        for cp in data["controlledPumps"]:
            p = station.get_pump_from_id(UUID.UUID(cp["id"]))
            if p != None:
                controlledPumps[p.get_id()] = p

        return Thermostat(data["pin"], data["name"], UUID.UUID(data["id"]), controlledPumps)