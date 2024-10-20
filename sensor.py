"""Platform for sensor integration."""

from __future__ import annotations
from datetime import datetime

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.const import UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from .const import DOMAIN, HeatPumpType

# from .heatpump_engine import heatpump_engine
from .heatpump_engine import HeatPumpMode, my_heatpump_engine, HeatPumpGenStatus


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
    hass.states.set(DOMAIN + ".controller_mac", "-")
    hass.states.set(DOMAIN + ".heat_circuit_mode", "-")
    hass.states.set(DOMAIN + ".hot_water_mode", "-")
    # main states
    hass.states.set(DOMAIN + ".operational_status", "-")
    hass.states.set(DOMAIN + ".system_uptime", "-")
    hass.states.set(DOMAIN + ".heat_pump_type", "-")
    hass.states.set(DOMAIN + ".software_version", "-")
    hass.states.set(DOMAIN + ".biv_level", "-")
    hass.states.set(DOMAIN + ".compact", "-")
    hass.states.set(DOMAIN + ".comfort", "-")
    # my_heatpump_engine.host = str(config["ser2net-host"])
    # my_heatpump_engine.port = int(config["ser2net-port"])


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
        self.main_wp_type_cache = HeatPumpType.UNKNOWN
        self.main_sw_status_cache = "-"
        self.main_biv_level_cache = -1
        self.main_status_cache = HeatPumpGenStatus.UNKNOWN
        self.main_sys_uptime_cache = datetime.fromisoformat("2000-01-01T00:05:23")
        self.main_compact_cache = -1
        self.main_comfort_cache = -1
        self.controller_mac_addr_cache = "-"

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

        if self.main_wp_type_cache != my_heatpump_engine.main_wp_type:
            self.hass.states.set(
                DOMAIN + ".heat_pump_type", my_heatpump_engine.main_wp_type.name
            )
            self.main_wp_type_cache = my_heatpump_engine.main_wp_type

        if self.main_sw_status_cache != my_heatpump_engine.main_sw_status:
            self.hass.states.set(
                DOMAIN + ".software_version", my_heatpump_engine.main_sw_status
            )
            self.main_sw_status_cache = my_heatpump_engine.main_sw_status

        if self.main_biv_level_cache != my_heatpump_engine.main_biv_level:
            self.hass.states.set(
                DOMAIN + ".biv_level", my_heatpump_engine.main_biv_level
            )
            self.main_biv_level_cache = my_heatpump_engine.main_biv_level

        if self.main_status_cache != my_heatpump_engine.main_status:
            self.hass.states.set(
                DOMAIN + ".operational_status", my_heatpump_engine.main_status.name
            )
            self.main_status_cache = my_heatpump_engine.main_status

        if self.main_sys_uptime_cache != my_heatpump_engine.main_sys_uptime:
            self.hass.states.set(
                DOMAIN + ".system_uptime", my_heatpump_engine.main_sys_uptime
            )
            self.main_sys_uptime_cache = my_heatpump_engine.main_sys_uptime

        if self.main_compact_cache != my_heatpump_engine.main_compact:
            self.hass.states.set(DOMAIN + ".compact", my_heatpump_engine.main_compact)
            self.main_compact_cache = my_heatpump_engine.main_compact

        if self.main_comfort_cache != my_heatpump_engine.main_comfort:
            self.hass.states.set(DOMAIN + ".comfort", my_heatpump_engine.main_comfort)
            self.main_comfort_cache = my_heatpump_engine.main_comfort

        if self.controller_mac_addr_cache != my_heatpump_engine.mac_id:
            self.hass.states.set(DOMAIN + ".controller_mac", my_heatpump_engine.mac_id)
            self.controller_mac_addr_cache = my_heatpump_engine.mac_id
            # if self._attr_unique_id != my_heatpump_engine.mac_id:
            #    self._attr_unique_id = my_heatpump_engine.mac_id


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
