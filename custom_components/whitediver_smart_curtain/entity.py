from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr

from .const import DOMAIN
from .device import SmartCurtainDevice


class SmartCurtainDeviceEntity:

    def __init__(self, device: SmartCurtainDevice, hass: HomeAssistant):
        """Init entity with the device"""
        self._attr_unique_id = \
            f'{device.mac}_{self.__class__.__name__}'
        self.device: SmartCurtainDevice = device
        self.hass = hass

    @property
    def device_info(self):
        """Shared device info information"""
        return {
            'identifiers': {(DOMAIN, self.device.mac)},
            'connections': {
                (dr.CONNECTION_NETWORK_MAC, self.device.mac)
            },
            'name': self.device.name,
            'manufacturer': 'Whitediver',
            'model': self.device.model
        }
