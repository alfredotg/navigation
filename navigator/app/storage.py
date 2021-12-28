import networkx
import random
from app.schemas import Route
from typing import Optional
from networkx.algorithms.shortest_paths.generic import \
        shortest_path_length as nx_shortest_path_length, \
        shortest_path as nx_shortest_path

G = networkx.Graph()

def clear():
    G = networkx.Graph()

def init():
    for x in range(0, 1000):
        for y in range(0, 1000):
            for i in [(1, 0), (0, 1)]:
                add_edge(point_id(x, y), point_id(x + i[0], y + i[1]), weight=int(random.random() * 10))

def add_edge(a_id: int, b_id: int, weight: int):
    G.add_edge(a_id, b_id, weight=weight)


def point_id(x: int, y: int) -> int:
    if y > 1_000:
        raise Exception("id overflow: %d, x: %d, y: %d" % (id, x, y))
    return x * 1_000 + y


def shortest_path(from_id: int, to_id: int) -> Optional[Route]:
    try:
        points = nx_shortest_path(G, source=from_id, target=to_id, weight="weight")
        if points is None or len(points) == 0:
            return None
        return Route(points = points, length = nx_shortest_path_length(G, source=from_id, target=to_id, weight="weight"))
    except networkx.exception.NetworkXNoPath:
        return None
    except networkx.exception.NodeNotFound:
        return None
