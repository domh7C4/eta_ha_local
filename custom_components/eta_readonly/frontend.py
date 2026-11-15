# SPDX-License-Identifier: GPL-3.0-only
"""Register the card resource only. Never create dashboards or sidebar panels."""
import logging
from urllib.parse import urlsplit
from homeassistant.components.lovelace import LOVELACE_DATA

_LOGGER = logging.getLogger(__name__)
LOGO_URL = "/eta_readonly/eta-logo.png"
CARD_PATH = "/eta_readonly/eta-heating-card.js"
CARD_URL = CARD_PATH + "?v=1.0.1"


async def async_setup_card_resource(hass):
    data = hass.data.get(LOVELACE_DATA)
    if data is None:
        return
    if data.resource_mode != "storage":
        _LOGGER.warning("Lovelace-Ressourcen sind YAML-verwaltet. %s als type: module ergänzen", CARD_URL)
        return
    resources = data.resources
    # Public info method ensures that the storage collection has been loaded.
    await resources.async_get_info()
    for item in resources.async_items():
        if urlsplit(item.get("url", "")).path == CARD_PATH:
            if item.get("url") != CARD_URL or item.get("type") != "module":
                await resources.async_update_item(item["id"], {"url": CARD_URL, "res_type": "module"})
            return
    await resources.async_create_item({"url": CARD_URL, "res_type": "module"})
