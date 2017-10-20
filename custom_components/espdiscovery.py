import logging
import homeassistant.util.dt as dt
import homeassistant.helpers.event as events
from homeassistant.helpers.discovery import load_platform
from homeassistant.loader import get_component
import homeassistant.loader as loader

import homeassistant.components.persistent_notification as pn


#import voluptuous as vol
#import homeassistant.helpers.config_validation as cv
#from homeassistant.components.climate import PLATFORM_SCHEMA
from datetime import timedelta


DOMAIN = "espdiscovery"
SENS_TO_SW = "sens_to_switch"
DEPENDENCIES = ["mqtt"]

_LOGGER = logging.getLogger(__name__)


CONF_MIN_TEMP = 'min_temp'
CONF_MAX_TEMP = 'max_temp'
CONF_TARGET_TEMP = 'target_temp'
CONF_MIN_DUR = 'min_cycle_duration'
CONF_TOLERANCE = 'tolerance'


#PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
#    vol.Optional(CONF_MAX_TEMP): vol.Coerce(float),
#    vol.Optional(CONF_MIN_TEMP): vol.Coerce(float),
#    vol.Optional(CONF_MIN_DUR): vol.All(cv.time_period, cv.positive_timedelta),
#    #vol.Optional(CONF_TARGET_TEMP): vol.Coerce(float),
#    vol.Optional(CONF_TOLERANCE, default=DEFAULT_TOLERANCE): vol.Coerce(float),
#})


def setup(hass, config):
    
    cfg = config.get(DOMAIN)

#    print(cfg)
#    clim_opts = {
#            "max_temp" : cfg.get(CONF_MAX_TEMP),
#            "min_temp" : cfg.get(CONF_MIN_TEMP),
#            "min_cycle_duration" : cfg.get(CONF_MIN_DUR),
#            "target_temp" : cfg.get(CONF_MIN_TEMP),
#            "tolerance" : cfg.get(CONF_TOLERANCE),
#        }

    clim_opts = {
            "max_temp" : cfg["max_temp"],
            "min_temp" : cfg["min_temp"],
            "min_cycle_duration" : cfg["min_cycle_duration"],
            "target_temp" : cfg["min_temp"],
            "tolerance" : cfg["tolerance"],
        }
    
    sens_to_switch_map = cfg.get(SENS_TO_SW)
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
    
    
    """Setup the component."""
    discovered = {}
    
    interval = dt.dt.timedelta(seconds=5)
    timeout = 180

    mqtt = loader.get_component('mqtt')
    group = loader.get_component('group')
    persistent_notification = loader.get_component('persistent_notification')

    #topic = config[DOMAIN].get('topic', DEFAULT_TOPIC)
    #entity_id = 'hello_mqtt.last_message'
    topic = "espdiscovery"
    entity_id = ""

    thermo_ent = []
    thermo_grp = group.Group.create_group(hass, "Thermostats", 
            view=False, object_id="thermo")
    
    temp_ent = []
    temp_grp = group.Group.create_group(hass, "Temperature", 
            view=False, object_id="temperature")
    
    hum_ent = []
    hum_grp = group.Group.create_group(hass, "Humidity", 
            view=False, object_id="humidity")
    
    thermosw_ent = []
    thermosw_grp = group.Group.create_group(hass, "Thermostats Switches", 
            view=False, object_id="thermosw")
    
    thermobin_ent = []
    thermobin_grp = group.Group.create_group(hass, "Heaters Switches", 
            view=False, object_id="thermo_binse")
   

    def load_temp_sensors(deviceid):
       
        sens_name = "temp_{}".format(deviceid)
        ts_entity_id = "sensor.{}".format(sens_name)
        load_platform(hass, 'sensor', "espthermostat", {
            "deviceid" : deviceid,
            "type" : "temperature",
            "name" : sens_name,
            })
        temp_ent.append(ts_entity_id)
        
        return ts_entity_id


    def load_hum_sensors(deviceid):
       
        sens_name = "hum_{}".format(deviceid)
        hs_entity_id = "sensor.{}".format(sens_name)
        load_platform(hass, 'sensor', "espthermostat", {
            "deviceid" : deviceid,
            "type" : "humidity",
            "name" : sens_name,
            })
        hum_ent.append(hs_entity_id)
        
        return hs_entity_id
            
    
    def load_switch(deviceid, switchnr, hide):
        
        switch_name = "sw{}_{}".format(
            switchnr,
            deviceid,
            )
        sw_entity_id = "switch.{}".format(switch_name)
        load_platform(hass, 'switch', "espthermostat", {
            "deviceid" : deviceid,
            "name" : switch_name,
            "switchnr" : switchnr,
            "hide" : hide,
            })
        #res.append(sw_entity_id)
        
        if not hide:
            thermosw_ent.append(sw_entity_id)
        
        return sw_entity_id


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
  
        tp = load_temp_sensors(deviceid)
        res.append(tp)
        
        hs = load_hum_sensors(deviceid)
        res.append(hs)

        if dev_type == "std" or dev_type == "sen":
            
            sw0 = load_switch(deviceid, "0", True)
            res.append(sw0)

            sw1 = load_switch(deviceid, "1", False)
            res.append(sw1)
       
            if dev_type == "std":
                
                cl_entity_id = "climate.{}".format(deviceid)
                discovery_info = {
                        "deviceid" : deviceid,
                        "sw_id" : sw0,
                         "ts_id" : tp,
                        }
                for c in clim_opts:
                    discovery_info[c] = clim_opts[c]

                load_platform(
                        hass, 
                        'climate', 
                        "espthermostat",
                        discovery_info,
                    )
                res.append(cl_entity_id)
                thermo_ent.append(cl_entity_id)
            
            else: 
                
                sw_id, sw_nr = thermo_map[deviceid]
                sw_entity_id = "switch.sw{}_{}".format(sw_nr, sw_id)

                discovery_info = {
                        "deviceid" : deviceid,
                        "sw_id" : sw_entity_id,
                        "ts_id" : tp,
                        }
                for c in clim_opts:
                    discovery_info[c] = clim_opts[c]

                cl_entity_id = "climate.{}".format(deviceid)
                load_platform(
                        hass, 
                        'climate', 
                        "espthermostat",
                        discovery_info,
                        )
                res.append(cl_entity_id)
                thermo_ent.append(cl_entity_id)

        
        elif dev_type == "sw":
            
            sw0 = load_switch(deviceid, "0", True)
            res.append(sw0)

            sw1 = load_switch(deviceid, "1", True)
            res.append(sw1)
            
        thermo_grp.update_tracked_entity_ids(thermo_ent) 
        temp_grp.update_tracked_entity_ids(temp_ent)
        hum_grp.update_tracked_entity_ids(hum_ent)
        thermosw_grp.update_tracked_entity_ids(thermosw_ent)
        thermobin_grp.update_tracked_entity_ids(thermobin_ent) 

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

    events.async_track_time_interval(hass, periodic, interval)
    mqtt.subscribe(hass, topic, message_received)
    return True

