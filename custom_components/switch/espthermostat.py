import homeassistant.components.switch.mqtt as mqsw
from homeassistant.helpers.entity import Entity

class HidableMQTTSW(mqsw.MqttSwitch):

    def __init__(self, hass, name, state_topic, command_topic, qos, retain,
            payload_on, payload_off, optimistic, value_template, hide):
        super().__init__(name, state_topic, command_topic, qos, retain,
                payload_on, payload_off, optimistic, value_template)

        self._hidden = hide

    @property
    def hidden(self) -> bool:
        return self._hidden



def setup_platform(hass, config, add_devices, discovery_info=None):
    
    deviceid = discovery_info["deviceid"]
    hide = discovery_info["hide"]
    switchnr = discovery_info["switchnr"]
    friendlyname = discovery_info["name"]

    mqttsw = HidableMQTTSW(
                 hass,
                 friendlyname,
                 "devices/{}/switch{}/state".format(
                     deviceid,
                     switchnr),
                 "devices/{}/switch{}/cmd".format(
                     deviceid,
                     switchnr),
                 0,
                 True,
                 "ON",
                 "OFF",
                 False,
                 None,
                 hide,
                 )
    add_devices([mqttsw])



