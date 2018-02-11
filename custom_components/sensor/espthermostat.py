import homeassistant.components.sensor.mqtt as mqse
from homeassistant.const import TEMP_CELSIUS

measure_unit = {
        "temperature" : TEMP_CELSIUS,
        "humidity" : "%",
}


class HidableMQTTSE(mqse.MqttSensor):


    def __init__(self, *args, **kwargs):
        self._hidden = kwargs.pop("hide")
        super(HidableMQTTSE, self).__init__(*args, **kwargs)
        return


    @property
    def hidden(self) -> bool:
        return self._hidden
    
    
def setup_platform(hass, config, add_devices, discovery_info=None):
    
    deviceid = discovery_info["deviceid"]
    sens_type = discovery_info["type"]
    sens_name = discovery_info["name"]


    # Listener to handle fired events
    def handle_event(event):
        se._hidden = event.data["hide"]
        se.schedule_update_ha_state()

    # Listen for when my_cool_event is fired
    hass.bus.listen("espthermo.{}".format(deviceid), handle_event)

    se = HidableMQTTSE(         
            sens_name,
            'devices/{}/{}'.format(
                deviceid,
                sens_type
                ),
            0,
            measure_unit[sens_type],
            False,
            120,
            None,
            hide=False,
            json_attributes="", 
            availability_topic=None, 
            payload_available="online",
            payload_not_available="offline"
            )

    add_devices([se])

