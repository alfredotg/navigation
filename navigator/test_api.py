import pytest
from main import app
from app import schemas, models, crud
from fastapi.testclient import TestClient
from app.database import SessionLocal 

client = TestClient(app)

def create_route(session, name: str, user_id: int, distance: int) -> models.Route:
    route = session.query(models.Route).filter(models.Route.name == name).first()
    if route is None:
        route = crud.create_route(
            session, 
            name=name,
            user_id=user_id,
            distance=distance,
            steps=[1, 2]
        )
    return route

@pytest.fixture(name="routes")
def routes_fixture():
    routes = []
    with SessionLocal() as session:
        session.query(models.Route).delete()
        routes.append(create_route(session, "alice first route", 100, 1))
        routes.append(create_route(session, "alice second route", 100, 20))
        routes.append(create_route(session, "bob route", 200, 5))
        yield routes


def test_save_route():
    steps = [1, 2, 3, 4]
    route = schemas.Route(
        name="First route",
        user_id=1,
        distance=15,
    )
    request = schemas.SaveRouteRequest(route=route, steps=steps)

    response = client.post(
        "/routes/save",
        json=request.dict()
    )
    assert response.status_code == 200
    json = response.json()
    assert json["uid"] > 0
    assert len(json["steps"]) == len(steps)
    
    filters = schemas.RouteFilters(ids=[json["uid"]], join_steps=True)
    
    find_response = client.post(
        "/routes/find",
        json=filters.dict()
    )
    assert find_response.status_code == 200
    routes = find_response.json()["items"]
    assert len(routes) == 1
    found = routes[0]
    assert json["uid"] == found["uid"]
    assert len(found["steps"]) == len(steps)
    assert found["user_id"] == route.user_id
    assert found["distance"] == route.distance

def test_stats(routes):
    response = client.get(
        "/routes/stats_by_users"
    )
    assert response.status_code == 200
    stats = response.json()["items"]
    assert stats[0]["count"] == 2
    assert stats[0]["distance"] == 21
    assert stats[1]["count"] == 1
    assert stats[1]["distance"] == 5 
