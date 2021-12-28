from guide import Client
from guide.api.default import make_route as api_make_route
from guide.models.route_response import RouteResponse
from typing import Optional

from .api import raise_on_errors

async def make_route(client: Client, from_id: int, to_id: int) -> Optional[RouteResponse]:
    response = await api_make_route.asyncio_detailed(from_id, to_id, client=client)
    raise_on_errors(response)
    if response.parsed.route is None:
        return None 
    return response.parsed
