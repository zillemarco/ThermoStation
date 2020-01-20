from app import app
from .models.station import Station
import json

@app.route('/thermostats')
def thermostats():
    st = Station()
    thermostats = st.get_thermostats()

    result = []
    for thermostat in thermostats:
        result.append(thermostat.to_json())

    return json.dumps(result)

@app.route('/pumps')
def pumps():
    st = Station()
    pumps = st.get_pumps()

    result = []
    for pump in pumps:
        result.append(pump.to_json())

    return json.dumps(result)