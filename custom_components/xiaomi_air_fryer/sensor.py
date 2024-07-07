"""Sensors of the Xiaomi AirFryer component."""

from enum import Enum
import logging

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfTemperature, UnitOfTime
from homeassistant.core import HomeAssistant

from .entity import AirFryerEntity
from .fryer_miot import Status

_LOGGER = logging.getLogger(__name__)


SENSOR_TYPES_MAF: tuple[SensorEntityDescription, ...] = (
    SensorEntityDescription(
        key="status",
        name="Status",
        device_class=SensorDeviceClass.ENUM,
        options=[status.name for status in Status],
    ),
    SensorEntityDescription(
        key="target_time",
        name="Target Time",
        device_class=SensorDeviceClass.DURATION,
        native_unit_of_measurement=UnitOfTime.MINUTES,
    ),
    SensorEntityDescription(
        key="target_temperature",
        name="Target Temperature",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="left_time",
        name="Left Time",
        device_class=SensorDeviceClass.DURATION,
        native_unit_of_measurement=UnitOfTime.MINUTES,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant, config_entry: ConfigEntry, async_add_entities
):
    """Set up the miio fan device from config."""
    coordinator = config_entry.runtime_data
    sensors = [
        XiaomiAirFryerSensor(config_entry, stype, coordinator)
        for stype in SENSOR_TYPES_MAF
    ]
    async_add_entities(sensors)


class XiaomiAirFryerSensor(AirFryerEntity, SensorEntity):
    """Xiaomi AirFryer Sensor."""

    @property
    def native_value(self):
        """Return the state."""
        value = getattr(self.coordinator.data, self.entity_description.key, None)
        if isinstance(value, Enum):
            return value.name
        return value
