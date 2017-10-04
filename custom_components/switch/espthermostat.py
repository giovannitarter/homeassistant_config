import homeassistant.components.switch.mqtt as mqsw
from homeassistant.helpers.entity import Entity


class HidableMQTTSW(mqsw.MqttSwitch):

    def __init__(self, *args, **kwargs):
        
        self._hidden = kwargs.pop("hide")
        super(HidableMQTTSW, self).__init__(*args, **kwargs)

    
    @property
    def hidden(self) -> bool:
        return self._hidden
    
   
    #@property
    #def state_attributes(self):
    #    """Return the attributes of the entity."""
    #    return self._attributes


def setup_platform(hass, config, add_devices, discovery_info=None):
    
    deviceid = discovery_info["deviceid"]
    hide = discovery_info["hide"]
    switchnr = discovery_info["switchnr"]
    friendlyname = discovery_info["name"]

    if hide == False:
        # Listener to handle fired events
        def handle_event(event):
            mqttsw._hidden = event.data["hide"]
            mqttsw.schedule_update_ha_state()

        # Listen for when my_cool_event is fired
        hass.bus.listen("espthermo.{}".format(deviceid), handle_event)
    
    mqttsw = HidableMQTTSW(
                 #hass=hass,
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



