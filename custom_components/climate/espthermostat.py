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
    max_temp = discovery_info["max_temp"]
    min_temp = discovery_info["min_temp"]
    min_cycle_duration = timedelta(seconds=discovery_info["min_cycle_duration"])
    target_temp = discovery_info["target_temp"]
    tolerance = discovery_info["tolerance"]
    ac_mode = False
    
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
