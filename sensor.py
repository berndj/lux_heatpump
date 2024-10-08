"""Platform for sensor integration."""

from __future__ import annotations

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.const import UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from .const import DOMAIN

# from .heatpump_engine import heatpump_engine
from .heatpump_engine import HeatPumpMode, my_heatpump_engine


class Peer:
    """Representation of the ser2net peer."""

    def __init__(self, host, port) -> None:
        """Init sensor."""
        self.host = host
        self.port = port

    def set_peer(self, host, port):
        """Set the peer."""

        if self.host != host or self.port != port:
            self.port = port
            self.host = host
        return self.host, self.port

    def get_peer(self):
        """Get the current peer."""

        return self.host, self.port


peer = Peer("baba-cafe", 4322)


def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up the sensor platform."""
    add_entities([HeatpumpSensor1()])
    add_entities([HeatpumpSensor2()])
    add_entities([HeatpumpSensor3()])
    add_entities([HeatpumpSensor4()])
    add_entities([HeatpumpSensor5()])
    add_entities([HeatpumpSensor6()])
    host, port = peer.get_peer()

    hass.states.set(DOMAIN + ".controller_host", host)
    hass.states.set(DOMAIN + ".controller_port", port)
    hass.states.set(DOMAIN + ".heat_circuit_mode", "-")
    hass.states.set(DOMAIN + ".hot_water_mode", "-")


#    my_heatpump_engine.host = str(config["ser2net-host"])
#    my_heatpump_engine.port = int(config["ser2net-port"])


class HeatpumpSensor1(SensorEntity):
    """Representation of a Sensor."""

    _attr_name = "luxtronik1 Outdoor temperature"
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_unique_id = "baba-cafe:4322:1"

    def __init__(self) -> None:
        """Init sensor."""
        self.eng = my_heatpump_engine
        self.heat_mode_cache = HeatPumpMode.UNKNOWN
        self.hot_water_mode_cache = HeatPumpMode.UNKNOWN

    def update(self) -> None:
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """
        host, port = peer.get_peer()

        self.eng.poll_for_stats(host, port)
        self._attr_native_value = self.eng.outdoor_temp

        if self.heat_mode_cache != my_heatpump_engine.heat_circ_mode:
            self.hass.states.set(
                DOMAIN + ".heat_circuit_mode", my_heatpump_engine.heat_circ_mode.name
            )
            self.heat_mode_cache = my_heatpump_engine.heat_circ_mode

        if self.hot_water_mode_cache != my_heatpump_engine.hot_water_mode:
            self.hass.states.set(
                DOMAIN + ".hot_water_mode", my_heatpump_engine.hot_water_mode.name
            )
            self.hot_water_mode_cache = my_heatpump_engine.hot_water_mode


class HeatpumpSensor2(SensorEntity):
    """Representation of a Sensor."""

    _attr_name = "luxtronik1 heating circuit flow temperature"
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_unique_id = "baba-cafe:4322:2"

    def __init__(self) -> None:
        """Init sensor."""
        self.eng = my_heatpump_engine

    def update(self) -> None:
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant .
        """
        host, port = peer.get_peer()
        self.eng.poll_for_stats(host, port)
        self._attr_native_value = self.eng.heating_circuit_flow_temp


class HeatpumpSensor3(SensorEntity):
    """Representation of a Sensor."""

    _attr_name = "luxtronik1 heating circuit return flow temperature (actual)"
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_unique_id = "baba-cafe:4322:3"

    def __init__(self) -> None:
        """Init sensor."""
        self.eng = my_heatpump_engine

    def update(self) -> None:
        """Fetch new state data for the sensor.

        update_peer(host,port)
        This is the only method that should fetch new data for Home Assistant.
        """
        host, port = peer.get_peer()
        self.eng.poll_for_stats(host, port)
        self._attr_native_value = self.eng.heating_circuit_return_flow_temp_actual


class HeatpumpSensor4(SensorEntity):
    """Representation of a Sensor."""

    _attr_name = "luxtronik1 heating circuit return flow temperature (setpoint)"
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_unique_id = "baba-cafe:4322:4"

    def __init__(self) -> None:
        """Init sensor."""
        self.eng = my_heatpump_engine

    def update(self) -> None:
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """
        host, port = peer.get_peer()
        self.eng.poll_for_stats(host, port)
        self._attr_native_value = self.eng.heating_circuit_return_flow_temp_setpoint


class HeatpumpSensor5(SensorEntity):
    """Representation of a Sensor."""

    _attr_name = "luxtronik1 hot water temperature (actual)"
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_unique_id = "baba-cafe:4322:5"

    def __init__(self) -> None:
        """Init sensor."""
        self.eng = my_heatpump_engine

    def update(self) -> None:
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """
        host, port = peer.get_peer()
        self.eng.poll_for_stats(host, port)
        self._attr_native_value = self.eng.domestic_hot_water_temp_actual


class HeatpumpSensor6(SensorEntity):
    """Representation of a Sensor."""

    _attr_name = "luxtronik1 hot water temperature (setpoint)"
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_unique_id = "baba-cafe:4322:6"

    def __init__(self) -> None:
        """Init sensor."""
        self.eng = my_heatpump_engine

    def update(self) -> None:
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """
        host, port = peer.get_peer()
        self.eng.poll_for_stats(host, port)
        self._attr_native_value = self.eng.domestic_hot_water_temp_setpoint
