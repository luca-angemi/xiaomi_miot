"""Select of the Xiaomi AirFryer component."""
# pylint: disable=import-error
import asyncio
import logging
from enum import Enum
from typing import Optional
from datetime import timedelta

from homeassistant.components.select import SelectEntity, SelectEntityDescription
from homeassistant.components.sensor import ENTITY_ID_FORMAT
from homeassistant.core import callback
from homeassistant.helpers import device_registry as dr
from homeassistant.util import slugify
from homeassistant.exceptions import PlatformNotReady
from homeassistant.const import (
    CONF_HOST,
    CONF_MAC,
    CONF_TOKEN,
    UnitOfTemperature,
    UnitOfTime,
)

from miio import Device, DeviceException
from .const import (
    CONF_MODEL,
    DATA_KEY,
    DATA_STATE,
    DOMAIN,
    MODELS_CARELI,
    MODELS_ALL_DEVICES
)

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(seconds=10)

SELECT_TYPES_MAF = {
    "target_time": ["Target Time", None, "target_time", UnitOfTime.MINUTES, "mdi:menu", None, ['3','5','10','15', '17', '20','25','30']],
    "target_temperature": ["Target Temperature", None, "target_temperature", UnitOfTemperature.CELSIUS, None, None, ['130','150', '170', '180','190','200']],
}


async def async_setup_entry(hass, config, async_add_entities, discovery_info=None):
    """Set up the miio fan device from config."""

    if DATA_KEY not in hass.data:
        hass.data[DATA_KEY] = {}

    if config.data.get(CONF_HOST, None):
        host = config.data[CONF_HOST]
        token = config.data[CONF_TOKEN]
        model = config.data.get(CONF_MODEL)
    else:
        host = config.options[CONF_HOST]
        token = config.options[CONF_TOKEN]
        model = config.options.get(CONF_MODEL)

    _LOGGER.info("Initializing with host %s (token %s...)", host, token[:5])

    if model is None:
        try:
            miio_device = Device(host, token)
            device_info = await hass.async_add_executor_job(miio_device.info)
            model = device_info.model
            _LOGGER.info(
                "%s %s %s detected",
                model,
                device_info.firmware_version,
                device_info.hardware_version,
            )
        except DeviceException as ex:
            raise PlatformNotReady from ex

    selects = []
    fryer = hass.data[DOMAIN][host]
    if model in MODELS_CARELI:
        for stype in SELECT_TYPES_MAF.values():
            selects.append(XiaomiAirFryerSelect(fryer, host, stype, config))
    else:
        _LOGGER.error(
            "Unsupported device found! Please create an issue at "
            "https://github.com/tsunglung/XiaomiAirFryer/issues "
            "and provide the following data: %s",
            model,
        )
        return False

    async_add_entities(selects, True)


class XiaomiAirFryerSelect(SelectEntity):
    """ Xiaomi AirFryer Sensor """
    def __init__(self, device, host, config, entry):
        """Initialize sensor."""
        self._device = device
        self._host = host
        self._model = entry.options.get(CONF_MODEL)
        self._mac = entry.options[CONF_MAC]
        self._device_id = entry.unique_id
        self._device_name = entry.title
        self._attr_name = config[0]
        self._child = config[1]
        self._attr = config[2]
        self._attr_options = config[6]
        self._attr_unique_id = "{}.{}-{}".format(
            DOMAIN, entry.unique_id, self._attr_name.lower().replace(" ", "-"))

        self.entity_id = ENTITY_ID_FORMAT.format(
            "{}_{}".format(DOMAIN, slugify(self._attr_name))
        )

    @property
    def current_option(self) -> str | None:
        """Retrieve currently selected option."""
        state = self.hass.data[DATA_KEY][self._host].get(DATA_STATE, None)

        if self._child is not None:
            state = getattr(state, self._child, None)
            # Unset state if child attribute isn't available anymore
            if state is None:
                return None

        if state is not None:
            value = getattr(state, self._attr, None)
            if isinstance(value, Enum):
                return str(value.name)
            else:
                return str(value)

    async def async_select_option(self, option: str) -> None:
        """Set the current option."""
        
        if 'temperature' in self._attr:
            self._device.target_temperature(int(option))
        else:
            self._device.target_time(int(option))

    @property
    def device_info(self):
        """Return the device info."""
        device_info = {
            "identifiers": {(DOMAIN, self._device_id)},
            "manufacturer": (self._model or "Xiaomi").split(".", 1)[0].capitalize(),
            "name": self._device_name,
            "model": self._model,
        }

        if self._mac is not None:
            device_info["connections"] = {(dr.CONNECTION_NETWORK_MAC, self._mac)}

        return device_info

