import logging

from homeassistant.components.number import NumberEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .device import SmartCurtainDevice
from .entity import SmartCurtainDeviceEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
        hass: HomeAssistant, entry: ConfigEntry,
        async_add_entities: AddEntitiesCallback):
    curtain_device: SmartCurtainDevice = hass.data[DOMAIN][entry.unique_id]
    async_add_entities([
        SmartCurtainWidthEntity(curtain_device, hass),
        SmartCurtainPositionEntity(curtain_device, hass)
    ])
    return True


class SmartCurtainWidthEntity(SmartCurtainDeviceEntity, NumberEntity):

    _attr_name = 'Maximum width'
#    _attr_native_min_value = 0
#    _attr_native_step = 1
    _attr_mode = 'box'

    @property
    def _attr_native_value(self):
        return self.device.max_width

    async def async_set_native_value(self, value: float) -> None:
        """Update the current value."""
        self.device.max_width = value
        await self.device.reset_max_width()


class SmartCurtainPositionEntity(SmartCurtainDeviceEntity, NumberEntity):

    _attr_name = 'Position to update'
#    _attr_native_min_value = 0
#    _attr_native_max_value = 100
    _attr_native_step = 1

    @property
    def _attr_native_value(self):
        return self.device.current_cover_position

    async def async_set_native_value(self, value: float) -> None:
        """Update the current value."""
        self.device.current_cover_position = value
        await self.device.reset_position()
