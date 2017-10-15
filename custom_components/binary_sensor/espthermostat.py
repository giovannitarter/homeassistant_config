import homeassistant.components.binary_sensor.template as bs
from datetime import timedelta


class HidableBST(bs.BinarySensorTemplate):

    def __init__(self, *args, **kwargs):
        self._hidden = kwargs.pop("hide")
        super(HidableBST, self).__init__(*args, **kwargs)
        return

    @property
    def hidden(self) -> bool:
        return self._hidden
    
    
def setup_platform(hass, config, add_devices, discovery_info=None):
    
    deviceid = discovery_info["deviceid"]
    name = discovery_info["name"]
    sw_id = discovery_info["switch_id"]
    template_str = "{{ is_state('{}', 'on') }}".format(sw_id)

    # Listener to handle fired events
    def handle_event(event):
        bst._hidden = event.data["hide"]
        bst.schedule_update_ha_state()

    # Listen for when my_cool_event is fired
    hass.bus.listen("espthermo.{}".format(deviceid), handle_event)

    bst = HidableBST(
            hass=hass, 
            device=deviceid, 
            friendly_name=name, 
            device_class=None,
            value_template=template_str, 
            entity_ids=[sw_id], 
            delay_on=timedelta(seconds=0), 
            delay_off=timedelta(seconds=0),
            hide=False
            )

    add_devices([bst])

