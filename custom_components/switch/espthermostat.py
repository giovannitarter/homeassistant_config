import homeassistant.components.switch.mqtt as mqsw
from homeassistant.helpers.entity import Entity

class HidableMQTTSW(mqsw.MqttSwitch):

    def __init__(self, hass, name, state_topic, command_topic, availability_topic,
                    qos, retain, payload_on, payload_off, optimistic,
                    payload_available, payload_not_available, value_template, hide):
    
        super().__init__(name, state_topic, command_topic, availability_topic,
                    qos, retain, payload_on, payload_off, optimistic,
                    payload_available, payload_not_available, value_template)

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
                 hass=hass,
                 name=friendlyname,
                 state_topic="devices/{}/switch{}/state".format(
                     deviceid,
                     switchnr),
                 command_topic="devices/{}/switch{}/cmd".format(
                     deviceid,
                     switchnr),
                 availability_topic="devices/{}/switch{}/avail".format(
                     deviceid,
                     switchnr),
                 qos=0,
                 retain=True,
                 payload_on="ON",
                 payload_off="OFF",
                 optimistic=False,
                 payload_available="ON",
                 payload_not_available="OFF",
                 value_template=None,
                 hide=hide,
                 )
    add_devices([mqttsw])



