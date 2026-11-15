# SPDX-License-Identifier: GPL-3.0-only
"""Local ETA heating integration with optional API write access."""
import asyncio
from datetime import timedelta
import logging
import math
from time import monotonic
from pathlib import Path
import aiohttp
from homeassistant.const import Platform
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.helpers import config_validation as cv
from homeassistant.exceptions import HomeAssistantError, ServiceValidationError
from .api import EtaClient
from .const import DOMAIN
from .scan import read_points
from .control import write_payload
from .services import async_setup_services
from .frontend import LOGO_URL, CARD_PATH, async_setup_card_resource
from homeassistant.components.http import StaticPathConfig

PLATFORMS = [Platform.SENSOR, Platform.SELECT]
_LOGGER = logging.getLogger(__name__)
CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)


async def async_setup(hass, config):
    async_setup_services(hass)
    await hass.http.async_register_static_paths([
        StaticPathConfig(LOGO_URL, str(Path(__file__).parent / "brand" / "logo.png"), True),
        StaticPathConfig(CARD_PATH, str(Path(__file__).parent / "www" / "eta-heating-card.js"), True),
    ])
    try:
        await async_setup_card_resource(hass)
    except (HomeAssistantError, ValueError) as err:
        _LOGGER.error("ETA-Kartenressource konnte nicht registriert werden: %s", err)
    return True

class EtaCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, entry):
        super().__init__(hass, _LOGGER, name=DOMAIN,
                         update_interval=timedelta(seconds=entry.data["interval"]))
        self.client = EtaClient(async_get_clientsession(hass), entry.data["host"], entry.data["port"])
        self.points = entry.data["points"]
        self.entry = entry
        self.write_info = {}
        self._write_lock = asyncio.Lock()

    @property
    def write_enabled(self):
        return self.entry.options.get("allow_write", False)

    async def async_load_write_info(self):
        if self.write_enabled:
            self.write_info = await read_points(
                self.points, self.client.varinfo,
                errors=(aiohttp.ClientError, TimeoutError, ValueError, OSError))

    async def async_write(self, uri, value, *, raw=False, begin=None, end=None):
        async with self._write_lock:
            if not self.write_enabled:
                raise ServiceValidationError("Schreibzugriff ist in den Integrationsoptionen deaktiviert")
            if uri not in self.points:
                raise ServiceValidationError("Unbekannter oder nicht ausgewählter Datenpunkt")
            try:
                # Always obtain current permissions immediately before a write.
                info = await self.client.varinfo(uri)
                payload = write_payload(info, value, raw=raw, begin=begin, end=end)
            except ValueError as err:
                raise ServiceValidationError(str(err)) from err
            except (aiohttp.ClientError, OSError, TimeoutError) as err:
                raise HomeAssistantError("Schreibberechtigung nicht abrufbar; kein Wert geschrieben") from err
            if not self.write_enabled:
                raise ServiceValidationError("Schreibzugriff wurde inzwischen deaktiviert")
            try:
                await self.client.write(uri, payload)
            except (aiohttp.ClientError, OSError, TimeoutError, ValueError) as err:
                raise HomeAssistantError(
                    "Schreibauftrag nicht bestätigt. Zustand an der Heizung prüfen; "
                    "der Auftrag wird nicht automatisch wiederholt.") from err
        await self.async_request_refresh()

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
    await coordinator.async_load_write_info()
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True

async def async_unload_entry(hass, entry):
    if await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)
        return True
    return False
