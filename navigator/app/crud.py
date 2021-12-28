from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func

from . import models, schemas
from typing import Optional, List, Iterator

def fake_point(x: int, y: int) -> models.Point:
    return models.Point(point_id=(x * 1000 + y), name="%dx%d point" % (x, y))

def fake_point_by_id(point_id: int) -> models.Point:
    x = int(point_id / 1000)
    y = point_id % 1000
    return fake_point(x, y)

def select_all_points(_db: Session) -> Iterator[models.Point]:
    for x in range(0, 10):
        for y in range(0, 10):
            yield fake_point(x, y)

def find_points_by_ids(_db: Session, ids: List[int]) -> Iterator[models.Point]:
    for point_id in ids:
        yield fake_point_by_id(point_id)

def find_routes(db: Session, ids: Optional[List[int]], join_steps: bool) -> Iterator[models.Route]:
    query = db.query(models.Route)
    if ids is not None:
        query.filter(models.Route.route_id.in_(ids))
    if join_steps:
        query.options(joinedload(models.Route.route_step_collection))
    return query.yield_per(20)

def find_stats_by_users(db: Session) -> Iterator[schemas.RoutesStatsByUser]:
    query = db.query(
            models.Route.user_id, 
            func.count('*'), 
            func.sum(models.Route.distance)
        ).group_by(models.Route.user_id)
    for record in query.yield_per(20):
        yield schemas.RoutesStatsByUser(user_id=record[0], count=record[1], distance=record[2])

def create_route(db: Session, name: str, user_id: int, distance: int, steps: List[int]) -> models.Route:
    route_model = models.Route(
        name=name,
        user_id=user_id,
        from_id=steps[0],
        to_id=steps[-1],
        distance=distance
    )
    for point_id in steps:
        step = models.RouteStep(point_id=point_id, route=route_model)
        route_model.route_step_collection.append(step)
    db.add(route_model)
    db.commit()
    db.refresh(route_model)
    return route_model
