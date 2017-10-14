import homeassistant.components.climate.generic_thermostat as gt
from datetime import timedelta


class HidableGenericThermostat(gt.GenericThermostat):


    def __init__(self, *args, **kwargs):
        self._hidden = kwargs.pop("hide")
        super(HidableGenericThermostat, self).__init__(*args, **kwargs)


    @property
    def hidden(self) -> bool:
        return self._hidden
    
    
def setup_platform(hass, config, add_devices, discovery_info=None):
    
    deviceid = discovery_info["deviceid"]
    
    heater_entity_id = discovery_info["sw_id"]
    sensor_entity_id = discovery_info["ts_id"]
    min_temp = 13
    max_temp = 24
    target_temp = 13
    ac_mode = False
    min_cycle_duration = timedelta(seconds = 30)
    tolerance = 0.5
    
    # Listener to handle fired events
    def handle_event(event):
        mythermo._hidden = event.data["hide"]
        mythermo.schedule_update_ha_state()

    # Listen for when my_cool_event is fired
    hass.bus.listen("espthermo.{}".format(deviceid), handle_event)

    mythermo = HidableGenericThermostat(
            hass=hass, 
            name=deviceid, 
            heater_entity_id=heater_entity_id, 
            sensor_entity_id=sensor_entity_id, 
            min_temp=min_temp, 
            max_temp=max_temp,
            target_temp=target_temp, 
            ac_mode=ac_mode, 
            min_cycle_duration=min_cycle_duration,
            tolerance=tolerance,
            keep_alive=None,
            hide=False
            )

    add_devices([mythermo])
