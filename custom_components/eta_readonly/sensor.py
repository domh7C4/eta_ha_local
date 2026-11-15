# SPDX-License-Identifier: GPL-3.0-only
"""ETA values as numeric or textual Home Assistant sensors."""
from homeassistant.components.sensor import SensorEntity, SensorDeviceClass, SensorStateClass
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.device_registry import DeviceInfo
from .const import DOMAIN

CLASSES = {"°C": SensorDeviceClass.TEMPERATURE, "bar": SensorDeviceClass.PRESSURE,
           "kW": SensorDeviceClass.POWER, "W": SensorDeviceClass.POWER,
           "kWh": SensorDeviceClass.ENERGY, "Wh": SensorDeviceClass.ENERGY}

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(EtaSensor(coordinator, uri, name) for uri, name in coordinator.points.items())

class EtaSensor(CoordinatorEntity, SensorEntity):
    _attr_has_entity_name = True

    def __init__(self, coordinator, uri, name):
        super().__init__(coordinator)
        self.uri = uri
        self._attr_name = name
        self._attr_unique_id = f"{coordinator.entry.entry_id}_{uri}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, coordinator.entry.entry_id)}, manufacturer="ETA",
            name="ETA Heizung", configuration_url=coordinator.client.base)

    @property
    def reading(self):
        return (self.coordinator.data or {}).get(self.uri)

    @property
    def available(self):
        return super().available and self.reading is not None

    @property
    def native_value(self):
        return self.reading["state"] if self.reading else None

    @property
    def native_unit_of_measurement(self):
        return self.reading["unit"] or None if self.reading else None

    @property
    def device_class(self):
        return CLASSES.get(self.native_unit_of_measurement)

    @property
    def state_class(self):
        if self.device_class in (SensorDeviceClass.TEMPERATURE, SensorDeviceClass.PRESSURE, SensorDeviceClass.POWER):
            return SensorStateClass.MEASUREMENT
        return None

    @property
    def extra_state_attributes(self):
        if not self.reading:
            return {"uri": self.uri}
        return {"uri": self.uri, **{key: self.reading[key] for key in
                ("raw", "formatted", "scale_factor", "text_offset")}}
