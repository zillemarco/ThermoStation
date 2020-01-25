from app import app
from app.models.station import Station
from app.models.pump import Pump
from app.models.thermostat import Thermostat

import time
import RPi.GPIO as GPIO

RELAY_1 = 12
RELAY_2 = 11
RELAY_3 = 13
RELAY_4 = 15
THERMOSTAT_1_PIN = 7

station = Station()
station.read_configuration()

# station.add_thermostat(Thermostat(THERMOSTAT_1_PIN, "Termostato camera", 1, 20))
# station.add_pump(Pump(RELAY_1, "Radiatore salotto nord"))
# station.add_pump(Pump(RELAY_2, "Radiatore salotto sud", 8, 0, 16, 52))
# station.get_thermostat(0).add_controlled_pump(station.get_pump(0))
# station.get_thermostat(0).add_controlled_pump(station.get_pump(1))
# station.save_configuration()

if __name__ == '__main__':
    port = 5000
    app.run(host='0.0.0.0', port=port)