"""Select of the Xiaomi AirFryer component."""
import logging

from homeassistant.components.select import SelectEntity, SelectEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .entity import AirFryerEntity

_LOGGER = logging.getLogger(__name__)


SELECT_TYPES_MAF: tuple[SelectEntityDescription, ...] = (
    SelectEntityDescription(
        key="target_time",
        name="Target Time",
        options=["3", "5", "10", "15", "17", "20", "25", "30"],
    ),
    SelectEntityDescription(
        key="target_temperature",
        name="Target Temperature",
        options=["130", "150", "170", "180", "190", "200"],
    ),
)


async def async_setup_entry(
    hass: HomeAssistant, config_entry: ConfigEntry, async_add_entities
):
    """Set up the miio fan device from config."""
    coordinator = config_entry.runtime_data
    selects = [
        XiaomiAirFryerSelect(config_entry, stype, coordinator)
        for stype in SELECT_TYPES_MAF
    ]

    async_add_entities(selects, True)


class XiaomiAirFryerSelect(AirFryerEntity, SelectEntity):
    """Xiaomi AirFryer Sensor."""

    @property
    def current_option(self) -> str | None:
        """Retrieve currently selected option."""
        value = getattr(self.coordinator.data, self.entity_description.key, None)
        _LOGGER.debug("Got new state: %s", value)
        return str(value)

    async def async_select_option(self, option: str) -> None:
        """Set the current option."""
        getattr(self.coordinator.api, self.entity_description.key)(int(option))
        await self.coordinator.async_refresh()
