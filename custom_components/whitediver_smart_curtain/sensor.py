'''
Created on 19 мар. 2022 г.

@author: info
'''
from __future__ import annotations

import logging

from homeassistant.components.sensor import (SensorDeviceClass, SensorEntity,
                                             SensorStateClass)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import POWER_WATT
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .device import SmartCurtainDeviceBLE, SmartCurtainDeviceWiFi
from .entity import SmartCurtainDeviceEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
        hass: HomeAssistant, entry: ConfigEntry,
        async_add_entities: AddEntitiesCallback):
    """Set up a oiot consumption sensor."""
    curtain_device: SmartCurtainDevice = hass.data[DOMAIN][entry.unique_id]

    async_add_entities([
        SmartCurtainPowerSensor(curtain_device, hass),
        SmartCurtainSuccessSensor(curtain_device, hass),
        SmartCurtainPercentageSensor(curtain_device, hass),
        SmartCurtainErrorSensor(curtain_device, hass)
    ])
    return True


class SmartCurtainPowerSensor(SmartCurtainDeviceEntity, SensorEntity):

    _attr_name = 'Power level DAC'
    _attr_native_unit_of_measurement = POWER_WATT
    _attr_device_class = SensorDeviceClass.POWER
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_value = 0

    async def async_update(self):
        try:
            self._attr_native_value = await self.hass.async_add_executor_job(self.device.get_battery)
        except TypeError:
            _LOGGER.warn('type error')


class SmartCurtainSuccessSensor(SmartCurtainDeviceEntity, SensorEntity):

    _attr_name = 'Success counter'
    _attr_native_value = 0

    async def async_update(self):
        self._attr_native_value = self.device.success_count


class SmartCurtainErrorSensor(SmartCurtainDeviceEntity, SensorEntity):

    _attr_name = 'Error counter'
    _attr_native_value = 0

    async def async_update(self):
        self._attr_native_value = self.device.error_count


class SmartCurtainPercentageSensor(SmartCurtainDeviceEntity, SensorEntity):

    _attr_name = 'Availability'
    _attr_icon = 'mdi:percent'
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = '%'
    _attr_native_value = 0

    async def async_update(self):
        if (self.device.error_count + self.device.success_count) > 0:
            self._attr_native_value = 100 * self.device.success_count / \
                (self.device.error_count + self.device.success_count)
        else:
            self._attr_native_value = 0
