from unittest.mock import patch
import pytest

from main import app
from app.storage import point_id, add_edge, clear as clear_storage
from fastapi.testclient import TestClient

patch("app.storage.init")

client = TestClient(app)
                
@pytest.fixture
def add_edges():
    clear_storage()
    # connected
    add_edge(point_id(1, 1), point_id(1, 2), 1)
    add_edge(point_id(1, 2), point_id(1, 3), 1)
    add_edge(point_id(1, 3), point_id(2, 2), 3)

    # not connected
    add_edge(point_id(3, 3), point_id(4, 4), 1)

def test_node_not_found(add_edges):
    response = client.get(
        "/route/%d/%d" % (point_id(-1, -1), point_id(1, 2))
    )
    assert response.status_code == 200
    assert response.json()["route"] is None

def test_route_not_found(add_edges):
    response = client.get(
        "/route/%d/%d" % (point_id(1, 1), point_id(4, 4))
    )
    assert response.status_code == 200
    assert response.json()["route"] is None

def test_route_found(add_edges):
    response = client.get(
        "/route/%d/%d" % (point_id(1, 1), point_id(2, 2))
    )
    assert response.status_code == 200
    route = response.json()["route"]
    assert not route is None
    assert route["length"] == 5
