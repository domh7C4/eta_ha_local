# SPDX-License-Identifier: GPL-3.0-only
"""Register targeted write actions even if an entry is unavailable."""
import voluptuous as vol
from homeassistant.core import callback
from homeassistant.helpers import config_validation as cv, service
from .const import DOMAIN


@callback
def async_setup_services(hass):
    service.async_register_platform_entity_service(
        hass, DOMAIN, "set_value", entity_domain="sensor",
        schema={vol.Required("value"): vol.Coerce(str),
                vol.Optional("raw", default=False): cv.boolean,
                vol.Optional("begin"): vol.All(vol.Coerce(int), vol.Range(min=0, max=96)),
                vol.Optional("end"): vol.All(vol.Coerce(int), vol.Range(min=0, max=96))},
        func="async_set_eta_value",
    )
