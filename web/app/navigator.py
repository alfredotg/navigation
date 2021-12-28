from navigator import Client
from navigator.api.default import find_points as api_find_points, save_route as api_save_route, find_routes as api_find_routes, get_routes_stats_by_users as api_get_routes_stats_by_users
from navigator.models.filters import Filters 
from navigator.models.route_filters import RouteFilters
from navigator.models.route import Route 
from navigator.models.points import Points
from navigator.models.save_route_request import SaveRouteRequest
from navigator.models.routes_stats_by_user_list import RoutesStatsByUserList 
from typing import List

from .api import raise_on_errors

async def find_points(client: Client) -> Points:
    response = await api_find_points.asyncio_detailed(client=client, json_body=Filters())
    raise_on_errors(response)
    return response.parsed.items

# return encoded Route
async def save_route_raw(client: Client, route: Route, steps: List[int]) -> str:
    save_request = SaveRouteRequest(
        route=route, 
        steps=steps
    )
    response = await api_save_route.asyncio_detailed(json_body=save_request, client=client)
    raise_on_errors(response)
    return response.content

# return encoded Routes 
async def find_routes_raw(client: Client) -> str:
    response = await api_find_routes.asyncio_detailed(json_body=RouteFilters(join_steps=True), client=client)
    raise_on_errors(response)
    return response.content

async def get_routes_stats(client: Client) -> RoutesStatsByUserList:
    response = await api_get_routes_stats_by_users.asyncio_detailed(client=client)
    raise_on_errors(response)
    return response.parsed
