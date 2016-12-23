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
        
        load_platform(hass, 'switch', "espthermostat", {
            "deviceid" : deviceid,
            "switchnr" : "0",
            "name" : devicename,
            })
        
        load_platform(hass, 'switch', "espthermostat", {
            "deviceid" : deviceid,
            "switchnr" : "1",
            "name" : devicename,
            })
        
        load_platform(hass, 'sensor', "espthermostat", {
            "deviceid" : deviceid,
            "type" : "humidity",
            "name" : devicename,
            })
        
        load_platform(hass, 'sensor', "espthermostat", {
            "deviceid" : deviceid,
            "type" : "temperature",
            "name" : devicename,
            })
        
        load_platform(hass, 'climate', "espthermostat", {
            "name" : devicename,
            "deviceid" : deviceid,
            })
    
    
    def message_received(topic, payload, qos):
        #"""A new MQTT message has been received."""
        #hass.states.set(entity_id, payload)
        print("###############")
        print(payload)
        print("###############")
        
        if payload not in discovered:
            discovered.append(payload)
            espthermostat_discovered(payload)
    
    

    """Setup the component."""
    mqtt = loader.get_component('mqtt')
    #topic = config[DOMAIN].get('topic', DEFAULT_TOPIC)
    #entity_id = 'hello_mqtt.last_message'
    topic = "espdiscovery"
    entity_id = ""

    discovered = []
    mqtt.subscribe(hass, topic, message_received)

    return True

