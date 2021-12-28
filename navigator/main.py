from app.env import load_dotenv

load_dotenv()

from fastapi import FastAPI, Depends, HTTPException, status
from app import schemas, crud, mapper, models
from app.database import SessionLocal

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post(
    "/points/find", 
    response_model=schemas.Points, 
    operation_id="findPoints"
    )
def find_points(filters: schemas.Filters, db: SessionLocal = Depends(get_db)) \
        -> schemas.Points:
    response = schemas.Points(items=[])
    if filters.ids is None:
        points = crud.select_all_points(db)
    else:
        points = crud.find_points_by_ids(db, filters.ids)
    for point in points:
        response.items.append(mapper.point_to_dto(point))
    return response

@app.post(
    "/routes/save", 
    response_model=schemas.Route, 
    operation_id="saveRoute"
    )
def save_route(request: schemas.SaveRouteRequest, db: SessionLocal = Depends(get_db)) \
        -> schemas.Route:
    route = request.route
    if len(request.steps) < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Route's steps are empty"
        )
    route_model = crud.create_route(
        db, 
        name=route.name, 
        user_id=route.user_id, 
        distance=route.distance,
        steps=request.steps)
    return mapper.route_to_dto(route_model, True)

@app.post(
    "/routes/find", 
    response_model=schemas.Routes, 
    operation_id="findRoutes",
    description="Finds saved routes"
    )
def find_routes(filters: schemas.RouteFilters, db: SessionLocal = Depends(get_db)) \
        -> schemas.Points:
    response = schemas.Routes(items=[])
    response.items = []
    for route in crud.find_routes(db, filters.ids, filters.join_steps):
        response.items.append(mapper.route_to_dto(route, filters.join_steps))
    return response

@app.get(
    "/routes/stats_by_users", 
    response_model=schemas.RoutesStatsByUserList, 
    operation_id="getRoutesStatsByUsers",
    )
def get_routes_stats_by_users(db: SessionLocal = Depends(get_db)) \
        -> schemas.Points:
    response = schemas.RoutesStatsByUserList(items=[])
    response.items = []
    for record in crud.find_stats_by_users(db):
        response.items.append(record)
    return response
