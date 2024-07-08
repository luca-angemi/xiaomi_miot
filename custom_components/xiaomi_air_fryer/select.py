"""Select of the Xiaomi AirFryer component."""
import logging

from homeassistant.components.select import SelectEntity, SelectEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .entity import AirFryerEntity
from .fryer_miot import CookingMode

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
    SelectEntityDescription(
        key="recipe_id",
        name="Recipe Id",
        options=[mode.name for mode in CookingMode],
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
        value = str(getattr(self.coordinator.data, self.entity_description.key, None))
        return str(value.split('.')[-1])

    async def async_select_option(self, option: str) -> None:
        """Set the current option."""
        if self.entity_description.key == 'recipe_id':
            option = 'M' + str(CookingMode[option].value)
        else:
            option = int(option)        
        getattr(self.coordinator.api, self.entity_description.key)(option)
        await self.coordinator.async_refresh()
