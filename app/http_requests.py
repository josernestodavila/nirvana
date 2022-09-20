import aiohttp

JSON = int | str | float | bool | None | dict[str, "JSON"] | list["JSON"]
JSONObject = dict[str, JSON]
JSONList = list[JSON]


async def http_get(url: str, params=None) -> JSONObject:
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            return await response.json()
