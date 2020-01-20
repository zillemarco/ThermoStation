from app import app
from app.models.station import Station

import time
import RPi.GPIO as GPIO

RELAY_1 = 12
RELAY_2 = 11
RELAY_3 = 13
RELAY_4 = 15
THERMOSTAT_1_PIN = 7

def thermo_changed(thermo):
    station = Station()
    pump = station.get_pump(0)

    if thermo.is_on():
        pump.turn_on()
    else:
        pump.turn_off()

station = Station()
station.add_thermostat(THERMOSTAT_1_PIN, "Termostato camera")
station.add_pump(RELAY_1, "Radiatore salotto nord")
station.add_pump(RELAY_2, "Radiatore salotto sud")
station.get_thermostat(0).add_on_changed(thermo_changed)

if __name__ == '__main__':
    port = 5000
    app.run(host='0.0.0.0', port=port)