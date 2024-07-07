"""Entity representing a D-Link Power Plug device."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_MAC, CONF_MODEL
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.entity import EntityDescription
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.util import slugify

from .const import DOMAIN


class AirFryerEntity(CoordinatorEntity):
    """Representation of a D-Link Power Plug entity."""

    _attr_has_entity_name = True

    def __init__(
        self,
        config_entry: ConfigEntry,
        description: EntityDescription,
        coordinator,
    ) -> None:
        """Initialize a D-Link Power Plug entity."""
        super().__init__(coordinator)
        self._device_id = config_entry.unique_id
        self._model = config_entry.data[CONF_MODEL]
        self._mac = config_entry.data[CONF_MAC]
        self.entity_description = description
        self._attr_unique_id = slugify(
            DOMAIN + config_entry.data[CONF_MAC] + self.entity_description.key.lower()
        )
        self._attr_device_info = dr.DeviceInfo(
            identifiers={(DOMAIN, self._device_id)},
            manufacturer=(self._model or "Xiaomi").split(".", 1)[0].capitalize(),
            model=self._model,
            name=config_entry.title,
            connections={(dr.CONNECTION_NETWORK_MAC, self._mac)}
        )
