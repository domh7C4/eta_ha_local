# SPDX-License-Identifier: GPL-3.0-only
"""Expose API-declared writable text choices without guessing boiler controls."""
from decimal import Decimal, InvalidOperation
from homeassistant.components.select import SelectEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.device_registry import DeviceInfo
from .const import DOMAIN


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    entities = []
    for uri, info in coordinator.write_info.items():
        if (info and info["writable"] and info["type"] == "TEXT" and info["choices"]
                and len({item["label"] for item in info["choices"]}) == len(info["choices"])
                and all(item["label"] for item in info["choices"])):
            entities.append(EtaSelect(coordinator, uri, info))
    async_add_entities(entities)


class EtaSelect(CoordinatorEntity, SelectEntity):
    _attr_has_entity_name = True

    @property
    def extra_state_attributes(self):
        return {"eta_integration": DOMAIN, "eta_config_entry_id": self.coordinator.entry.entry_id,
                "write_access_enabled": self.coordinator.write_enabled}

    def __init__(self, coordinator, uri, info):
        super().__init__(coordinator)
        self.uri = uri
        self.info = info
        self._attr_name = coordinator.points[uri] + " einstellen"
        self._attr_unique_id = f"{coordinator.entry.entry_id}_{uri}_control"
        self._attr_options = [item["label"] for item in info["choices"]]
        self._attr_device_info = DeviceInfo(identifiers={(DOMAIN, coordinator.entry.entry_id)})

    @property
    def available(self):
        return (super().available and self.coordinator.write_enabled
                and (self.coordinator.data or {}).get(self.uri) is not None)

    @property
    def current_option(self):
        reading = (self.coordinator.data or {}).get(self.uri)
        if reading is None:
            return None
        try:
            raw = Decimal(reading["raw"])
        except InvalidOperation:
            return None
        for choice in self.info["choices"]:
            if Decimal(choice["raw"]) == raw:
                return choice["label"]
        return None

    async def async_select_option(self, option):
        await self.coordinator.async_write(self.uri, option)
