import logging
import homeassistant.util.dt as dt
import homeassistant.helpers.event as events
from homeassistant.helpers.discovery import load_platform
from homeassistant.loader import get_component
import homeassistant.loader as loader

import homeassistant.components.persistent_notification as pn


DOMAIN = "espdiscovery"
SENS_TO_SW = "sens_to_switch"
DEPENDENCIES = ["mqtt"]

_LOGGER = logging.getLogger(__name__)


def setup(hass, config):
    
    sens_to_switch_map = config[DOMAIN].get(SENS_TO_SW)
    sens_boards = []
    sw_boards = []
    thermo_map = {}

    if sens_to_switch_map is not None:
        for brd in sens_to_switch_map:
            
            se = brd["sensor"]
            if se not in sens_boards:
                sens_boards.append(se)

            sw = (brd["switch"], brd["switch_nr"])
            if sw not in sw_boards:
                sw_boards.append(sw)

            thermo_map[se] = sw

    
    def espthermostat_discovered(hostname):
      
        res = []
        deviceid = hostname

        dev_type = "std"
        if deviceid in sens_boards:
            dev_type = "sen"
        else:
            for sw_id, sw_nr in sw_boards:
                if deviceid == sw_id:
                    dev_type = "sw"
                    break

        if dev_type == "std" or dev_type == "sen":
            switchnr = "0"
            switch_name = "sw{}_{}".format(
                switchnr,
                deviceid,
                )
            sw0_entity_id = "switch.{}".format(switch_name)
            load_platform(hass, 'switch', "espthermostat", {
                "deviceid" : deviceid,
                "name" : switch_name,
                "switchnr" : switchnr,
                "hide" : True,
                })
            res.append(sw0_entity_id)
            thermosw_grp.update_tracked_entity_ids([sw0_entity_id])
            
            bins_entity_id = "binary_sensor.{}".format(deviceid)
            load_platform(
                    hass, 
                    "binary_sensor", 
                    "espthermostat", {
                        "deviceid" : deviceid,
                        "switch_id" : sw0_entity_id,
                        "name" : switch_name,
                        }
                    )
            res.append(bins_entity_id)
            thermobin_grp.update_tracked_entity_ids([bins_entity_id])

            switchnr = "1"
            switch_name = "sw{}_{}".format(
                switchnr,
                deviceid,
                )
            sw1_entity_id = "switch.{}".format(switch_name)
            load_platform(hass, 'switch', "espthermostat", {
                "deviceid" : deviceid,
                "name" : switch_name,
                "switchnr" : switchnr,
                "hide" : False,
                })
            res.append(sw1_entity_id)
            thermosw_grp.update_tracked_entity_ids([sw1_entity_id])
            
            bins_entity_id = "binary_sensor.{}".format(deviceid)
            load_platform(
                    hass, 
                    "binary_sensor", 
                    "espthermostat", {
                        "deviceid" : deviceid,
                        "switch_id" : sw1_entity_id,
                        "name" : switch_name,
                        }
                    )
            res.append(bins_entity_id)
            thermobin_grp.update_tracked_entity_ids([bins_entity_id])
            
            sens_name = "hum_{}".format(deviceid)
            hs_entity_id = "sensor.{}".format(sens_name)
            load_platform(hass, 'sensor', "espthermostat", {
                "deviceid" : deviceid,
                "type" : "humidity",
                "name" : sens_name,
                })
            res.append(hs_entity_id)
            hum_grp.update_tracked_entity_ids([hs_entity_id])

            sens_name = "temp_{}".format(deviceid)
            ts_entity_id = "sensor.{}".format(sens_name)
            load_platform(hass, 'sensor', "espthermostat", {
                "deviceid" : deviceid,
                "type" : "temperature",
                "name" : sens_name,
                })
            res.append(ts_entity_id)
            temp_grp.update_tracked_entity_ids([ts_entity_id])
       
            if dev_type == "std":
                cl_entity_id = "climate.{}".format(deviceid)
                load_platform(hass, 'climate', "espthermostat", {
                    "deviceid" : deviceid,
                    "sw_id" : sw0_entity_id,
                    "ts_id" : ts_entity_id,
                    })
                res.append(cl_entity_id)
                thermo_grp.update_tracked_entity_ids([cl_entity_id])
            
            else: 
                
                sw_id, sw_nr = thermo_map[deviceid]
                sw_entity_id = "switch.sw{}_{}".format(sw_nr, sw_id)

                cl_entity_id = "climate.{}".format(deviceid)
                load_platform(hass, 'climate', "espthermostat", {
                    "deviceid" : deviceid,
                    "sw_id" : sw_entity_id,
                    "ts_id" : ts_entity_id,
                    })
                res.append(cl_entity_id)
                thermo_grp.update_tracked_entity_ids([cl_entity_id])

        
        elif dev_type == "sw":
            switchnr = "0"
            switch_name = "sw{}_{}".format(
                switchnr,
                deviceid,
                )
            sw0_entity_id = "switch.{}".format(switch_name)
            load_platform(hass, 'switch', "espthermostat", {
                "deviceid" : deviceid,
                "name" : switch_name,
                "switchnr" : switchnr,
                "hide" : True,
                })
            res.append(sw0_entity_id)
            thermosw_grp.update_tracked_entity_ids([sw0_entity_id])
            
            bins_entity_id = "binary_sensor.{}".format(deviceid)
            load_platform(
                    hass, 
                    "binary_sensor", 
                    "espthermostat", {
                        "deviceid" : deviceid,
                        "switch_id" : sw0_entity_id,
                        "name" : switch_name,
                        }
                    )
            res.append(bins_entity_id)
            thermobin_grp.update_tracked_entity_ids([bins_entity_id])
            
            switchnr = "1"
            switch_name = "sw{}_{}".format(
                switchnr,
                deviceid,
                )
            sw1_entity_id = "switch.{}".format(switch_name)
            load_platform(hass, 'switch', "espthermostat", {
                "deviceid" : deviceid,
                "name" : switch_name,
                "switchnr" : switchnr,
                "hide" : True,
                })
            res.append(sw1_entity_id)
            thermosw_grp.update_tracked_entity_ids([sw1_entity_id])
            
            bins_entity_id = "binary_sensor.{}".format(deviceid)
            load_platform(
                    hass, 
                    "binary_sensor", 
                    "espthermostat", {
                        "deviceid" : deviceid,
                        "switch_id" : sw1_entity_id,
                        "name" : switch_name,
                        }
                    )
            res.append(bins_entity_id)
            thermobin_grp.update_tracked_entity_ids([bins_entity_id])
       
        return res
    
    
    def message_received(topic, payload, qos):
        #"""A new MQTT message has been received."""
        #hass.states.set(entity_id, payload)
 
        entry = discovered.get(payload) 
        
        if entry is None:
            entities = espthermostat_discovered(payload)
        else:
            time, entities, active = entry
            hass.bus.fire("espthermo.{}".format(payload), {"hide":False})
            
            #for e in entities:
            #    if e.find("sw0") == -1 :
            #        _LOGGER.info("UNHIDING entity {}".format(e))
        discovered[payload] = (dt.utcnow(), entities, True)
  

    def periodic(firetime):
        
        for p in discovered:
            
            last_update, entries, active = discovered[p] 

            delta = firetime - last_update
            if active:
                if delta.total_seconds() > timeout:
                    discovered[p] = (last_update, entries, False)
                    _LOGGER.info("HIDING thermo {}".format(p))
                    pn.create(hass, "thermo {} disappeared".format(p), "THERMO")
                    hass.bus.fire("espthermo.{}".format(p), {"hide":True})
                    #for e in entries:
                    #    _LOGGER.info("HIDING entity {}".format(e))
                        
        return


    """Setup the component."""
    discovered = {}
    
    interval = dt.dt.timedelta(seconds=5)
    timeout = 180
    events.async_track_time_interval(hass, periodic, interval)

    mqtt = loader.get_component('mqtt')
    group = loader.get_component('group')
    persistent_notification = loader.get_component('persistent_notification')

    #topic = config[DOMAIN].get('topic', DEFAULT_TOPIC)
    #entity_id = 'hello_mqtt.last_message'
    topic = "espdiscovery"
    entity_id = ""

    thermo_grp = group.Group.create_group(hass, "Thermostats", 
            view=False, object_id="thermo")
    temp_grp = group.Group.create_group(hass, "Temperature", 
            view=False, object_id="temperature")
    hum_grp = group.Group.create_group(hass, "Humidity", 
            view=False, object_id="humidity")
    thermosw_grp = group.Group.create_group(hass, "Thermostats Switches", 
            view=False, object_id="thermosw")
    thermobin_grp = group.Group.create_group(hass, "Heaters Switches", 
            view=False, object_id="thermo_binse")
    
    mqtt.subscribe(hass, topic, message_received)

    return True

