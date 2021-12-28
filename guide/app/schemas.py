from pydantic import BaseModel
from typing import List, Optional

class Route(BaseModel):
    distance: int
    points: List[int]

class RouteResponse(BaseModel):
    route: Optional[Route]
