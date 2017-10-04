import logging
import homeassistant.util.dt as dt
import homeassistant.helpers.event as events
from homeassistant.helpers.discovery import load_platform
from homeassistant.loader import get_component
import homeassistant.loader as loader

import homeassistant.components.persistent_notification as pn


DOMAIN = 'espdiscovery'
DEPENDENCIES = ['mqtt']

_LOGGER = logging.getLogger(__name__)


def setup(hass, config):
    
    
    def espthermostat_discovered(hostname):
      
        res = []
        deviceid = hostname 
        devicename = deviceid
        
        switchnr = "0"
        switch_name = "sw{}_{}".format(
            switchnr,
            devicename,
            )
        sw0_entity_id = "switch.{}".format(switch_name)
        load_platform(hass, 'switch', "espthermostat", {
            "deviceid" : deviceid,
            "name" : switch_name,
            "switchnr" : switchnr,
            "hide" : True,
            })
        res.append(sw0_entity_id)

        switchnr = "1"
        switch_name = "sw{}_{}".format(
            switchnr,
            devicename,
            )
        sw1_entity_id = "switch.{}".format(switch_name)
        load_platform(hass, 'switch', "espthermostat", {
            "deviceid" : deviceid,
            "name" : switch_name,
            "switchnr" : switchnr,
            "hide" : False,
            })
        res.append(sw1_entity_id)
       
        sens_name = "hum_{}".format(deviceid)
        hs_entity_id = "sensor.{}".format(sens_name)
        load_platform(hass, 'sensor', "espthermostat", {
            "deviceid" : deviceid,
            "type" : "humidity",
            "name" : sens_name,
            })
        res.append(hs_entity_id)

        sens_name = "temp_{}".format(deviceid)
        ts_entity_id = "sensor.{}".format(sens_name)
        load_platform(hass, 'sensor', "espthermostat", {
            "deviceid" : deviceid,
            "type" : "temperature",
            "name" : sens_name,
            })
        res.append(ts_entity_id)
        
        cl_entity_id = "clim_{}".format(deviceid)
        load_platform(hass, 'climate', "espthermostat", {
            "name" : devicename,
            "deviceid" : deviceid,
            "sw_id" : sw0_entity_id,
            "ts_id" : ts_entity_id,
            })
        res.append(cl_entity_id)

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

        hument = ["sensor.hum_{}".format(d) for d in discovered]
        tempent = ["sensor.temp_{}".format(d) for d in discovered]
        humgrp.update_tracked_entity_ids(hument)
        tempgrp.update_tracked_entity_ids(tempent)
  

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

    tempgrp = group.Group.create_group(hass, "Temperature", view=False)
    humgrp = group.Group.create_group(hass, "Humidity", view=False)
    
    mqtt.subscribe(hass, topic, message_received)

    return True

