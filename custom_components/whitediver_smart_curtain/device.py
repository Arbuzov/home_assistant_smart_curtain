'''
Created on 19 мар. 2022 г.

@author: info
'''
from binascii import hexlify
import logging

from homeassistant.backports.enum import StrEnum
from homeassistant.const import CONF_MAC, CONF_NAME
from homeassistant.helpers import device_registry as dr
import pygatt

from .const import DOMAIN


_LOGGER = logging.getLogger(__name__)


class SmartCurtainDeviceEntity:
    """Entity class for the Delonghi devices"""

    def __init__(self, device):
        """Init entity with the device"""
        self._attr_unique_id = \
            f'{device.mac}_{self.__class__.__name__}'
        self.device: SmartCurtainDevice = device

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


class SmartCurtainDevice:
    """Delongi Primadonna class"""

    def __init__(self, config: dict) -> None:
        """Initialize."""
        self.mac = config.get(CONF_MAC)
        self.name = config.get(CONF_NAME)
        self.model = 'Smart curtain'
        self.friendly_name = ''
        self.adapter = pygatt.GATTToolBackend()
        self.error_count = 0
        self.success_count = 0

    def get_voltage(self):
        result = 0
        uuid = "00002a19-0000-1000-8000-00805f9b34fb"
        self.adapter.start(reset_on_start=False)

        try:
            device = self.adapter.connect(self.mac, timeout=20)
            result = int.from_bytes(device.char_read(uuid), byteorder='little')
            _LOGGER.info("Read UUID %s: %d", uuid, result)
            self.success_count = self.success_count + 1
        except pygatt.exceptions.NotificationTimeout:
            _LOGGER.warn("Read UUID %s: failed with timeout", uuid)
            self.error_count = self.error_count + 1
        except pygatt.exceptions.NotConnectedError:
            _LOGGER.warn("Read UUID %s: failed cause disconnected", uuid)
            self.error_count = self.error_count + 1
        finally:
            self.adapter.stop()
        return result
