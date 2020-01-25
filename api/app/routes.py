from app import app
from flask import request
from .models.station import Station
from .models.pump import Pump
from .models.thermostat import Thermostat
from flask_cors import cross_origin
import json
import uuid as UUID

# Thermostats routes
@app.route('/thermostats')
@cross_origin()
def thermostats():
    st = Station()
    thermostats = st.get_thermostats()

    result = []
    for thermostat in thermostats:
        result.append(thermostat.to_json())

    return json.dumps(result)

@app.route('/thermostat/<thermostat_id>/status')
@cross_origin()
def thermostat_status(thermostat_id):
    st = Station()
    thermostat = st.get_thermostat_from_id(UUID.UUID(thermostat_id))

    if thermostat != None:
        return json.dumps(thermostat.get_status())
    return None

@app.route('/thermostat/<thermostat_id>', methods=['POST'])
@cross_origin()
def thermostat_edit(thermostat_id):
    st = Station()
    thermostat = st.get_thermostat_from_id(UUID.UUID(thermostat_id))
    
    if thermostat != None:
        thermostat.set_name(request.json["name"])
        thermostat.set_pin(int(request.json["pin"]))
        thermostat.set_type(int(request.json["type"]))
        thermostat.set_target_temperature(int(request.json["targetTemperature"]))

        thermostat.clear_controlled_pumps()

        for cp in request.json["controlledPumps"]:
            pump = st.get_pump_from_id(UUID.UUID(cp))
            if pump != None:
                thermostat.add_controlled_pump(pump)

        st.save_configuration()
        
        return json.dumps({ 'status': True })
    return json.dumps({ 'status': False })

@app.route('/thermostats/add', methods=['POST'])
@cross_origin()
def thermostat_add():
    st = Station()

    controlledPumps = {}
    for cp in request.json["controlledPumps"]:
        pump = st.get_pump_from_id(UUID.UUID(cp))
        if pump != None:
            controlledPumps[pump.get_id()] = pump

    thermostat = Thermostat(int(request.json["pin"]), request.json["name"], request.json["type"], request.json["targetTemperature"], None, controlledPumps)
    st.add_thermostat(thermostat)
    st.save_configuration()

    return json.dumps(thermostat.to_json())

@app.route('/thermostat/<thermostat_id>', methods=['DELETE'])
@cross_origin()
def thermostat_delete(thermostat_id):
    st = Station()
    if st.remove_thermostat(UUID.UUID(thermostat_id)):
        st.save_configuration()
        return json.dumps({ 'status': True })
    return json.dumps({ 'status': False })

# Pumps routes
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
        pump.change_start_and_stop_time(int(request.json["stopHour"]), int(request.json["stopMinute"]), int(request.json["startHour"]), int(request.json["startMinute"]))

        st.save_configuration()
        
        return json.dumps({ 'status': True })
    return json.dumps({ 'status': False })

@app.route('/pumps/add', methods=['POST'])
@cross_origin()
def pump_add():
    st = Station()
    pump = Pump(int(request.json["pin"]), request.json["name"], int(request.json["stopHour"]), int(request.json["stopMinute"]), int(request.json["startHour"]), int(request.json["startMinute"]))
    st.add_pump(pump)
    st.save_configuration()

    return json.dumps(pump.to_json())

@app.route('/pump/<pump_id>', methods=['DELETE'])
@cross_origin()
def pump_delete(pump_id):
    st = Station()
    if st.remove_pump(UUID.UUID(pump_id)):
        st.save_configuration()
        return json.dumps({ 'status': True })
    return json.dumps({ 'status': False })