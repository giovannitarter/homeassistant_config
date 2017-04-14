import homeassistant.components.sensor.mqtt as mqse
from homeassistant.const import TEMP_CELSIUS

shortNames = {
        "temperature" : "temp",
        "humidity" : "hum",
}

measure_unit = {
        "temperature" : TEMP_CELSIUS,
        "humidity" : "%",
}


def setup_platform(hass, config, add_devices, discovery_info=None):
    """Your switch/light specific code."""
    
    deviceid = discovery_info["deviceid"]
    senstype = discovery_info["type"]
    friendlyname = discovery_info["name"]

    sens_name = "{}_{}".format(
            shortNames[senstype],
            friendlyname,
            )
    sens_name = sens_name.upper()

    add_devices(
                [
                mqse.MqttSensor(
                    sens_name,
                    'devices/{}/{}'.format(
                        deviceid,
                        senstype 
                        ),
                    0,
                    measure_unit[senstype],
                    False,
		    120,
		    None	
                    ), 
                ])
    
