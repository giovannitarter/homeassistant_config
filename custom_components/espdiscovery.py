from homeassistant.components.discovery import load_platform
from homeassistant.loader import get_component
from homeassistant.helpers import discovery as hldisco
import homeassistant.loader as loader

DOMAIN = 'espdiscovery'
DEPENDENCIES = ['mqtt']


def setup(hass, config):
    
    
    def espthermostat_discovered(hostname):
      
        deviceid = hostname 
        devicename = deviceid[-4:].upper()
        
        switchnr = "0"
        switch_name = "sw{}_{}".format(
            switchnr,
            devicename,
            )
        entity_id = "switch.{}".format(switch_name)
        load_platform(hass, 'switch', "espthermostat", {
            "deviceid" : deviceid,
            "name" : switch_name,
            "switchnr" : switchnr,
            "hide" : True,
            })

        switchnr = "1"
        switch_name = "sw{}_{}".format(
            switchnr,
            devicename,
            )
        load_platform(hass, 'switch', "espthermostat", {
            "deviceid" : deviceid,
            "name" : switch_name,
            "switchnr" : switchnr,
            "hide" : False,
            })
        
        load_platform(hass, 'sensor', "espthermostat", {
            "deviceid" : deviceid,
            "type" : "humidity",
            "name" : devicename,
            })
        tempgrp.update_tracked_entity_ids(
                ["sensor.hum_{}".format(devicename)])
      

        load_platform(hass, 'sensor', "espthermostat", {
            "deviceid" : deviceid,
            "type" : "temperature",
            "name" : devicename,
            })
        humgrp.update_tracked_entity_ids(
                ["sensor.temp_{}".format(devicename)])
        

        load_platform(hass, 'climate', "espthermostat", {
            "name" : devicename,
            "deviceid" : deviceid,
            })
    
    
    def message_received(topic, payload, qos):
        #"""A new MQTT message has been received."""
        #hass.states.set(entity_id, payload)
        #print("###############")
        #print(payload)
        #print("###############")
        
        if payload not in discovered:
            discovered.append(payload)
            espthermostat_discovered(payload)
    
    

    """Setup the component."""
    mqtt = loader.get_component('mqtt')
    group = loader.get_component('group')
    persistent_notification = loader.get_component('persistent_notification')

    #topic = config[DOMAIN].get('topic', DEFAULT_TOPIC)
    #entity_id = 'hello_mqtt.last_message'
    topic = "espdiscovery"
    entity_id = ""

    #switches = group.Group.create_group(hass, "HeaterSW", view=True)
    tempgrp = group.Group.create_group(hass, "Temperature", view=False)
    humgrp = group.Group.create_group(hass, "Humidity", view=False)
    discovered = []
    mqtt.subscribe(hass, topic, message_received)

    return True

