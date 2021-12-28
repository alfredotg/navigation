from . import models, schemas, crud

def point_to_dto(point: models.Point) -> schemas.Point:
    return schemas.Point(uid=point.point_id, name=point.name)

def route_to_dto(route: models.Route, join_steps: bool) -> schemas.Route:
    schema = schemas.Route(
        uid=route.route_id,
        name=route.name,
        user_id=route.user_id,
        distance=route.distance
    )
    if join_steps:
        schema.steps = []
        for step in route.route_step_collection:
            schema.steps.append(point_to_dto(crud.fake_point_by_id(step.point_id)))
    return schema

def routes_stats_by_user_to_dto(record) -> schemas.RoutesStatsByUser:
    print(record)
    return schemas.RoutesStatsByUser(
            user_id=record.user_id,
            count=record.count,
            distance=record.distance
            )
