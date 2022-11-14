class SmartCurtainDevice:

    is_closed = False

    is_closing = False

    is_opening = False

    current_cover_position = 0

    async def get_battery(self):
        raise NotImplementedError

    async def open(self):
        raise NotImplementedError

    async def stop(self):
        raise NotImplementedError

    async def close(self):
        raise NotImplementedError

    async def set_position(self, position):
        raise NotImplementedError
