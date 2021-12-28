from unittest.mock import patch
import pytest

from main import app
from app.storage import get_point_id, add_edge, clear as clear_storage
from fastapi.testclient import TestClient

patch("app.storage.init")

client = TestClient(app)
                
@pytest.fixture(name="add_edges")
def fixture_add_edges():
    clear_storage()
    # connected
    add_edge(get_point_id(1, 1), get_point_id(1, 2), 1)
    add_edge(get_point_id(1, 2), get_point_id(1, 3), 1)
    add_edge(get_point_id(1, 3), get_point_id(2, 2), 3)

    # not connected
    add_edge(get_point_id(3, 3), get_point_id(4, 4), 1)

def test_node_not_found(_add_edges):
    response = client.get(
        "/route/%d/%d" % (get_point_id(-1, -1), get_point_id(1, 2))
    )
    assert response.status_code == 200
    assert response.json()["route"] is None

def test_route_not_found(_add_edges):
    response = client.get(
        "/route/%d/%d" % (get_point_id(1, 1), get_point_id(4, 4))
    )
    assert response.status_code == 200
    assert response.json()["route"] is None

def test_route_found(_add_edges):
    response = client.get(
        "/route/%d/%d" % (get_point_id(1, 1), get_point_id(2, 2))
    )
    assert response.status_code == 200
    route = response.json()["route"]
    assert not route is None
    assert route["length"] == 5
