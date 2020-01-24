from app import app
from flask import request
from .models.station import Station
from flask_cors import cross_origin
import json
import uuid as UUID

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

@app.route('/pump/<pump_id>/status')
@cross_origin()
def pump_status(pump_id):
    st = Station()
    pump = st.get_pump_from_id(UUID.UUID(pump_id))

    if pump != None:
        return json.dumps({ 'status': pump.is_on() })
    return None

@app.route('/pump/<pump_id>', methods=['POST'])
@cross_origin()
def pump_edit(pump_id):
    st = Station()
    pump = st.get_pump_from_id(UUID.UUID(pump_id))
    
    if pump != None:
        pump.set_name(request.json["name"])
        pump.set_pin(int(request.json["pin"]))

        st.save_configuration()
        
        return json.dumps({ 'status': True })
    return json.dumps({ 'status': False })

@app.route('/pumps/add', methods=['POST'])
@cross_origin()
def pump_add():
    st = Station()
    pump = Pump(int(request.json["pin"]), request.json["name"])
    st.add_pump(pump)

    return json.dumps(pump.to_json())

@app.route('/pump/<pump_id>', methods=['DELETE'])
@cross_origin()
def pump_delete(pump_id):
    st = Station()
    if st.remove_pump(UUID.UUID(pump_id)):
        st.save_configuration()
        return json.dumps({ 'status': True })
    return json.dumps({ 'status': False })