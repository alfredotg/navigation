from pydantic import BaseModel
from typing import List, Optional

class Token(BaseModel):
    access_token: str
    token_type: str

class Profile(BaseModel):
    uid: int
    name: str

class Profiles(BaseModel):
    items: List[Profile]

class Point(BaseModel):
    uid: int
    name: str

class Points(BaseModel):
    items: List[Point]

class Route(BaseModel):
    uid: Optional[int]
    name: str
    user_id: int
    distance: int
    steps: Optional[List[Point]]

class MakeRouteResponse(BaseModel):
    route: Optional[Route]

class Routes(BaseModel):
    items: List[Route]

class RoutesStatsByUser(BaseModel):
    user: Profile
    count: int
    distance: int

class RoutesStatsByUserList(BaseModel):
    items: List[RoutesStatsByUser]
