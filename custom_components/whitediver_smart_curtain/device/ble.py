import asyncio
import logging
from binascii import hexlify

import pygatt
from homeassistant.backports.enum import StrEnum
from homeassistant.const import CONF_MAC, CONF_NAME

from ..const import DOMAIN
from .abstract import SmartCurtainDevice

_LOGGER = logging.getLogger(__name__)


class SmartCurtainDeviceBLE(SmartCurtainDevice):
    """Delongi Primadonna class"""

    def __init__(self, config: dict) -> None:
        """Initialize."""
        self.mac = config.get(CONF_MAC)
        self.name = config.get(CONF_NAME)
        self.model = 'Smart curtain BLE'
        self.friendly_name = ''
        self.adapter = pygatt.GATTToolBackend()
        self.error_count = 0
        self.success_count = 0
        self.loop = asyncio.new_event_loop()

    def get_battery(self):
        _LOGGER.info("Nonblocking connection")
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
