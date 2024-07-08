"""Switch of the Xiaomi AirFryer component."""

from datetime import timedelta
import logging
from typing import Any

from miio import DeviceException

from homeassistant.components.switch import SwitchEntity, SwitchEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .entity import AirFryerEntity

_LOGGER = logging.getLogger(__name__)


SWITCH_TYPE = SwitchEntityDescription(
    key="switch",
)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the switch from a config entry."""
    coordinator = config_entry.runtime_data
    device = XiaomiAirFryer(config_entry, SWITCH_TYPE, coordinator)
    async_add_entities([device], True)


class XiaomiAirFryer(AirFryerEntity, SwitchEntity):
    """Representation of a Xiaomi AirFryer."""

    _attr_name = None

    def __init__(
        self,
        config_entry: ConfigEntry,
        description,
        coordinator,
    ) -> None:
        """Initialize a D-Link Power Plug entity."""
        super().__init__(config_entry, description, coordinator)
        
        self._state = self.coordinator.data.is_on

    @property
    def icon(self) -> str | None:
        """Return the icon to use for device if any."""
        return "mdi:pot-mix"

    @property
    def available(self) -> bool:
        """Return true when state is known."""
        return self.coordinator.data is not None

    @property
    def is_on(self) -> bool | None:
        """Return true if switch is on."""
        return self._state

    @callback
    def _handle_coordinator_update(self):
        """Fetch state from the device."""
        if self.coordinator.data is not None:
            self._state = self.coordinator.data.is_on
        self.async_write_ha_state()

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the air fryeron."""
        await self.hass.async_add_executor_job(self.coordinator.api.start_cook)
        self._state = True
        self.async_write_ha_state()


    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the air fryer off."""
        await self.hass.async_add_executor_job(self.coordinator.api.cancel_cooking)
        self._state = False
        self.async_write_ha_state()
