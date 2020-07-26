from .exceptions import PingError


class System:
    def __init__(self, api):
        self._api = api

    async def ping(self):
        result = await self._api.request("/rest/system/ping")
        if (
            not isinstance(result, dict)
            or "ping" not in result
            or result["ping"] != "pong"
        ):
            raise PingError
