import logging
import aiohttp

from homeassistant.const import CONF_MAC, CONF_NAME, CONF_IP_ADDRESS

from ..const import DOMAIN
from .abstract import SmartCurtainDevice


_LOGGER = logging.getLogger(__name__)


class SmartCurtainDeviceWiFi(SmartCurtainDevice):
    """Delongi Primadonna class"""

    def __init__(self, config: dict) -> None:
        """Initialize."""
        self.mac = config.get(CONF_MAC)
        self.name = config.get(CONF_NAME)
        self.ip = config.get(CONF_IP_ADDRESS)
        self.model = 'Smart curtain WiFi'
        self.friendly_name = ''
        self.error_count = 0
        self.success_count = 0
        self.state = {}

    def get_battery(self):
        self.state.get('battery')

    async def async_update(self):
        url = f"http://{self.ip}/api/status"
        session = aiohttp.ClientSession()
        resp = await session.get(url)
        self.state = await resp.json()
        await session.close()
        self.current_cover_position = self.state.get('position')
        self.is_closing = (self.state.get('direction') == 1)
        self.is_opening = (self.state.get('direction') == -1)
        self.is_closed = (self.state.get('position') < 1)

    async def open(self):
        url = f"http://{self.ip}/api/open"
        session = aiohttp.ClientSession()
        resp = await session.get(url)
        responce = await resp.json()
        self.is_opening = True
        self.is_closed = False
        await session.close()

    async def close(self):
        url = f"http://{self.ip}/api/close"
        session = aiohttp.ClientSession()
        resp = await session.get(url)
        responce = await resp.json()
        self.is_closing = True
        self.is_closed = False
        await session.close()

    async def stop(self):
        url = f"http://{self.ip}/api/stop"
        session = aiohttp.ClientSession()
        resp = await session.get(url)
        responce = await resp.json()
        self.is_closing = False
        self.is_opening = False
        await session.close()
