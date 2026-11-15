# SPDX-License-Identifier: GPL-3.0-only
"""Read-only ETA heating integration."""
from datetime import timedelta
import logging
import math
from time import monotonic
import aiohttp
from homeassistant.const import Platform
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from .api import EtaClient
from .const import DOMAIN
from .scan import read_points

PLATFORMS = [Platform.SENSOR]
_LOGGER = logging.getLogger(__name__)

class EtaCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, entry):
        super().__init__(hass, _LOGGER, name=DOMAIN,
                         update_interval=timedelta(seconds=entry.data["interval"]))
        self.client = EtaClient(async_get_clientsession(hass), entry.data["host"], entry.data["port"])
        self.points = entry.data["points"]
        self.entry = entry

    async def _async_update_data(self):
        start = monotonic()
        results = await read_points(
            self.points, self.client.value,
            errors=(aiohttp.ClientError, TimeoutError, ValueError, OSError))
        # Leave recovery time for large/slow installations instead of polling continuously.
        seconds = max(self.entry.data["interval"], math.ceil((monotonic() - start) * 1.5))
        self.update_interval = timedelta(seconds=seconds)
        if not any(item is not None for item in results.values()):
            raise UpdateFailed("Keine ETA-Datenpunkte erreichbar")
        return results

async def async_setup_entry(hass, entry):
    coordinator = EtaCoordinator(hass, entry)
    await coordinator.async_config_entry_first_refresh()
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True

async def async_unload_entry(hass, entry):
    if await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)
        return True
    return False
