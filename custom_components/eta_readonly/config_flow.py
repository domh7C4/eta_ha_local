# SPDX-License-Identifier: GPL-3.0-only
"""Discover actual controller points during the first setup."""
import ipaddress
import re
import aiohttp
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers import selector
from .api import EtaClient
from .const import DOMAIN
from .scan import read_points
from homeassistant.core import callback

READ_ERRORS = (aiohttp.ClientError, TimeoutError, ValueError, OSError)

class EtaConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return EtaOptionsFlow()

    def __init__(self):
        self._scan_task = None
        self._scan_error = None
        self.points = {}
        self.connection = {}
        self._found = {}

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            host = user_input["host"].strip().strip("[]").lower()
            try:
                ipaddress.ip_address(host)
                valid = True
            except ValueError:
                valid = bool(re.fullmatch(r"[a-z0-9](?:[a-z0-9.-]*[a-z0-9])?", host))
            if not valid:
                errors["base"] = "invalid_host"
            else:
                self._async_abort_entries_match({"host": host, "port": user_input["port"]})
                self.connection = {**user_input, "host": host}
                return await self.async_step_discover()
        return self.async_show_form(step_id="user", errors=errors, data_schema=vol.Schema({
            vol.Required("host"): str,
            vol.Required("port", default=8080): vol.All(vol.Coerce(int), vol.Range(min=1, max=65535)),
            vol.Required("interval", default=60): vol.All(vol.Coerce(int), vol.Range(min=30, max=3600)),
            vol.Optional("allow_write", default=False): bool,
        }))

    async def _async_discover(self):
        client = EtaClient(async_get_clientsession(self.hass), self.connection["host"], self.connection["port"])
        try:
            self.points = await client.menu()
            if not self.points:
                self._scan_error = "no_points"
                return
            readings = await read_points(self.points, client.value, errors=READ_ERRORS,
                                         progress=self.async_update_progress)
            self._found = {uri: name for uri, name in self.points.items() if readings[uri] is not None}
            if not self._found:
                self._scan_error = "no_points"
        except READ_ERRORS:
            self._scan_error = "cannot_connect"

    async def async_step_discover(self, user_input=None):
        if self._scan_task is None:
            self._scan_task = self.hass.async_create_task(self._async_discover())
        if not self._scan_task.done():
            return self.async_show_progress(step_id="discover", progress_action="discovering",
                                            progress_task=self._scan_task)
        self._scan_task.result()
        return self.async_show_progress_done(next_step_id="points")

    async def async_step_points(self, user_input=None):
        if self._scan_error:
            return self.async_abort(reason=self._scan_error)
        errors = {}
        if user_input is not None:
            selected = user_input["points"]
            if not selected or any(uri not in self._found for uri in selected):
                errors["base"] = "invalid_points"
            else:
                return self.async_create_entry(title=f"ETA {self.connection['host']}", data={
                    **{key: value for key, value in self.connection.items()
                       if key not in ("allow_write", "create_dashboard")},
                    "points": {uri: self._found[uri] for uri in selected},
                    "discovery": {"candidates": len(self.points), "readable": len(self._found),
                                  "skipped": len(self.points) - len(self._found)},
                }, options={"allow_write": self.connection.get("allow_write", False)})
        return self.async_show_form(
            step_id="points", errors=errors,
            description_placeholders={"found": str(len(self._found)),
                                      "skipped": str(len(self.points) - len(self._found))},
            data_schema=vol.Schema({
                vol.Required("points", default=list(self._found)): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=[{"value": uri, "label": f"{name} ({uri})"}
                                 for uri, name in self._found.items()],
                        multiple=True, mode=selector.SelectSelectorMode.DROPDOWN))
            }))


class EtaOptionsFlow(config_entries.OptionsFlowWithReload):
    async def async_step_init(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="", data={**self.config_entry.options, **user_input})
        return self.async_show_form(step_id="init", data_schema=vol.Schema({
            vol.Required("allow_write", default=self.config_entry.options.get("allow_write", False)): bool,
        }))
