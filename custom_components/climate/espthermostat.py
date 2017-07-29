import homeassistant.components.climate.generic_thermostat as gt
from datetime import timedelta

#gt.GenericThermostat(
#    hass, 
#    name, 
#    heater_entity_id, 
#    sensor_entity_id, 
#    min_temp, 
#    max_temp,
#    target_temp, 
#    ac_mode, 
#    min_cycle_duration
#    )


def setup_platform(hass, config, add_devices, discovery_info=None):
    """Your switch/light specific code."""
    name = discovery_info["name"]
    
    #heater_entity_id = discovery_info["heaterid"]
    #sensor_entity_id = discovery_info["sensorid"]
    
    #switch.sw0_fcb4
    #sensor.temp_fcb4
    heater_entity_id = "switch.sw0_{}".format(name).lower()
    sensor_entity_id = "sensor.temp_{}".format(name).lower()
    min_temp = 13
    max_temp = 24
    target_temp = 15
    ac_mode = False
    min_cycle_duration = timedelta(seconds = 10)
    tolerance = 0.5

    add_devices([
        gt.GenericThermostat(
            hass, 
            name, 
            heater_entity_id, 
            sensor_entity_id, 
            min_temp, 
            max_temp,
            target_temp, 
            ac_mode, 
            min_cycle_duration,
            tolerance,
            None
            )
        ]
        )

