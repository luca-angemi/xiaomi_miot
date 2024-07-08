"""Coordinator for Rova."""

from datetime import timedelta
import logging

from miio import DeviceException

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import DOMAIN
from .fryer_miot import FryerMiot

_LOGGER = logging.getLogger(__name__)

class AirFyerCoordinator(DataUpdateCoordinator):
    """Class to manage fetching Rova data."""

    def __init__(self, hass: HomeAssistant, api: FryerMiot) -> None:
        """Initialize."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=30),
        )
        self.api = api

    async def _async_update_data(self):
        """Fetch data from Rova API."""
        try:
            return await self.hass.async_add_executor_job(self.api.status)
        except DeviceException:
            return None
