import asyncio
from collections import defaultdict

import httpx
import msgspec

from model import OriginMap, RouteMap

client = httpx.AsyncClient()


async def get_jetblue_origins():
    url = "https://azrest.jetblue.com/od/od-service/origins?isLatLong=true"
    resp = await client.get(url)
    origins = msgspec.json.decode(resp.content, type=OriginMap).data.origins
    return [origin.code for origin in origins if origin.jb and not origin.cc]


async def get_direct_destinations(origin: str):
    url = f"https://www.jetblue.com/magnoliapublic/.rest/jetblue/v4/route-map/customDelivery/route/{origin}"

    resp = await client.get(url)
    try:
        routes = msgspec.json.decode(resp.content, type=RouteMap).routes
    except msgspec.ValidationError:
        if "error" in resp.json():
            return []
        else:
            print(f"Unexpected response for {origin}: {resp.text}")
            raise
    return [route.city3 for route in routes if route.city2 == "0"]


async def main():
    all_direct_routes = defaultdict(list)

    for origin in await get_jetblue_origins():
        for destination in await get_direct_destinations(origin):
            print(f"{origin} -> {destination}")
            all_direct_routes[origin].append(destination)

    with open("jetblue_routes.json", "wb") as f:
        f.write(msgspec.json.encode(all_direct_routes))


if __name__ == "__main__":
    asyncio.run(main())
