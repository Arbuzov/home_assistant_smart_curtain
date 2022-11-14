from pickle import NONE

from homeassistant.components.cover import (CoverDeviceClass, CoverEntity,
                                            CoverEntityFeature)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .device import SmartCurtainDevice
from .entity import SmartCurtainDeviceEntity


async def async_setup_entry(
        hass: HomeAssistant, entry: ConfigEntry,
        async_add_entities: AddEntitiesCallback):
    curtain_device: SmartCurtainDevice = hass.data[DOMAIN][entry.unique_id]

    async_add_entities([
        SmartCurtainCover(curtain_device, hass)
    ])
    return True


class SmartCurtainCover(SmartCurtainDeviceEntity, CoverEntity):

    device_class = CoverDeviceClass.SHADE
    supported_features = CoverEntityFeature.OPEN | CoverEntityFeature.CLOSE | CoverEntityFeature.SET_POSITION | CoverEntityFeature.STOP

    @property
    def _attr_is_closed(self):
        return self.device.is_closed

    @property
    def _attr_is_closing(self):
        return self.device.is_closing

    @property
    def _attr_is_opening(self):
        return self.device.is_opening

    @property
    def _attr_current_cover_position(self):
        return self.device.current_cover_position

    async def async_open_cover(self, **kwargs):
        """Open the cover."""
        await self.device.open()

    async def async_close_cover(self, **kwargs):
        """Close cover."""
        await self.device.close()

    async def async_set_cover_position(self, position):
        """Move the cover to a specific position."""
        await self.device.set_position(position)

    async def async_stop_cover(self, **kwargs):
        """Stop the cover."""
        await self.device.stop()

    async def async_update(self):
        await self.device.async_update()
