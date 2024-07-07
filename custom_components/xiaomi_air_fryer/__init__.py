"""The Xiaomi AirFryer component."""

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_MODEL, CONF_TOKEN, Platform
from homeassistant.core import HomeAssistant

from .coordinator import AirFyerCoordinator
from .fryer_miot import FryerMiot

_LOGGER = logging.getLogger(__name__)

PLATFORMS = [Platform.BUTTON, Platform.SELECT, Platform.SENSOR, Platform.SWITCH]

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Support Xiaomi AirFryer Component."""
    host = entry.data[CONF_HOST]
    token = entry.data[CONF_TOKEN]
    model = entry.data.get(CONF_MODEL)
    api = FryerMiot(host, token, model=model)

    coordinator = AirFyerCoordinator(hass, api)
    await coordinator.async_refresh()
    entry.runtime_data = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True
