import networkx
import random
from app.schemas import Route
from typing import Optional
from pydantic import BaseModel
from networkx.algorithms.shortest_paths.generic import \
        shortest_path_length as nx_shortest_path_length, \
        shortest_path as nx_shortest_path

MAX_DISTANCE = 100

G = networkx.Graph()

class Coords(BaseModel):
    x: int
    y: int
    
def clear():
    G.clear_edges()

def init():
    for x in range(0, 1000):
        for y in range(0, 1000):
            for i in [(1, 0), (0, 1)]:
                add_edge(get_point_id(x, y), get_point_id(x + i[0], y + i[1]), weight=int(random.random() * 10))

def add_edge(a_id: int, b_id: int, weight: int):
    G.add_edge(a_id, b_id, weight=weight)

def get_point_id(x: int, y: int) -> int:
    if y > 1_000:
        raise Exception("id overflow: %d, x: %d, y: %d" % (id, x, y))
    return x * 1_000 + y

def get_point_coords(point_id: int) -> Coords:
    return Coords(x=int(point_id/1000), y=point_id % 1000)

def shortest_path(from_id: int, to_id: int) -> Optional[Route]:
    from_coords = get_point_coords(from_id)
    to_coords = get_point_coords(to_id)
    if max(abs(from_coords.x - to_coords.x), abs(from_coords.y - to_coords.y)) > MAX_DISTANCE:
        return None

    try:
        points = nx_shortest_path(G, source=from_id, target=to_id, weight="weight")
        if points is None or len(points) == 0:
            return None
        return Route(points = points, distance = nx_shortest_path_length(G, source=from_id, target=to_id, weight="weight"))
    except networkx.exception.NetworkXNoPath:
        return None
    except networkx.exception.NodeNotFound:
        return None
