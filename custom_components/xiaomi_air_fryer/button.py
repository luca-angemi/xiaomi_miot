"""Button of the Xiaomi AirFryer component."""

import logging

from homeassistant.components.button import ButtonEntity, ButtonEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .entity import AirFryerEntity

_LOGGER = logging.getLogger(__name__)

BUTTON_TYPES_MAF: tuple[ButtonEntityDescription, ...] = (
    ButtonEntityDescription(
        key="cancel_cooking",
        name="Cancel Cooking",
    ),
    ButtonEntityDescription(
        key="start_cook",
        name="Start Cooking",
    ),
    ButtonEntityDescription(
        key="pause",
        name="Pause Cooking",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities,
):
    """Set up the miio fan device from config."""
    coordinator = config_entry.runtime_data
    buttons = [
        XiaomiAirFryerButton(config_entry, stype, coordinator)
        for stype in BUTTON_TYPES_MAF
    ]

    async_add_entities(buttons)


class XiaomiAirFryerButton(AirFryerEntity, ButtonEntity):
    """Xiaomi AirFryer Sensor."""

    async def async_press(self) -> None:
        """Triggers the restart."""
        getattr(self.coordinator.api, self.entity_description.key)()
        await self.coordinator.async_refresh()
