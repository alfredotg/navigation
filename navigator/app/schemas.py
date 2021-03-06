from pydantic import BaseModel
from typing import List, Optional

class Point(BaseModel):
    uid: int
    name: str

class Points(BaseModel):
    items: List[Point]

class Filters(BaseModel):
    ids: Optional[List[int]]

class RouteFilters(Filters):
    join_steps: bool

class Route(BaseModel):
    uid: Optional[int]
    name: str
    user_id: int
    distance: int
    steps: Optional[List[Point]]

class SaveRouteRequest(BaseModel):
    route: Route
    steps: List[int]

class Routes(BaseModel):
    items: List[Route]

class RoutesStatsByUser(BaseModel):
    user_id: int
    count: int
    distance: int

class RoutesStatsByUserList(BaseModel):
    items: List[RoutesStatsByUser]
