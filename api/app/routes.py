from app import app
from .models.station import Station
from flask_cors import cross_origin
import json

@app.route('/thermostats')
@cross_origin()
def thermostats():
    st = Station()
    thermostats = st.get_thermostats()

    result = []
    for thermostat in thermostats:
        result.append(thermostat.to_json())

    return json.dumps(result)

@app.route('/pumps')
@cross_origin()
def pumps():
    st = Station()
    pumps = st.get_pumps()

    result = []
    for pump in pumps:
        result.append(pump.to_json())

    return json.dumps(result)