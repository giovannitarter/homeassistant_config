import homeassistant.components.switch.mqtt as mqsw


def setup_platform(hass, config, add_devices, discovery_info=None):
    """Your switch/light specific code."""
    
    deviceid = discovery_info["deviceid"]
    switchnr = discovery_info["switchnr"]
    friendlyname = discovery_info["name"]

    switch_name = "sw{}_{}".format(
            switchnr,
            friendlyname,
            )

    switch_name = switch_name.upper()
    add_devices(
                [
                mqsw.MqttSwitch(
                    hass,
                    switch_name,
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
                    None
                    ),
                ]
                )

