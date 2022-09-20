from unittest.mock import patch

from fastapi import status
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_api_one():
    response = client.get("/api_one?member_id=1000")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"deductible": 1000, "stop_loss": 10000, "oop_max": 5000}


def test_api_one_no_member_id():
    response = client.get("/api_one")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_api_two():
    response = client.get("/api_two?member_id=1000")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"deductible": 1200, "stop_loss": 13000, "oop_max": 6000}


def test_api_two_no_member_id():
    response = client.get("/api_two")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_api_three():
    response = client.get("/api_three?member_id=1000")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"deductible": 1000, "stop_loss": 10000, "oop_max": 6000}


def test_api_three_no_member_id():
    response = client.get("/api_three")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_index():

    with patch('app.main.http_get') as mock_http_get:
        mock_http_get.side_effect = [
            {"deductible": 1000, "stop_loss": 10000, "oop_max": 5000},
            {"deductible": 1200, "stop_loss": 13000, "oop_max": 6000},
            {"deductible": 1000, "stop_loss": 10000, "oop_max": 6000},
        ]

        response = client.get("/?member_id=1000")

        assert mock_http_get.call_count == 3
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"deductible": 1066, "stop_loss": 11000, "oop_max": 5666}


def test_index_no_member_id():
    response = client.get("/")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_index_min_coalesce_strategy():
    with patch('app.main.http_get') as mock_http_get:
        mock_http_get.side_effect = [
            {"deductible": 1000, "stop_loss": 10000, "oop_max": 5000},
            {"deductible": 1200, "stop_loss": 13000, "oop_max": 6000},
            {"deductible": 1000, "stop_loss": 10000, "oop_max": 6000},
        ]

        response = client.get("/?member_id=1000&strategy=min")

        assert mock_http_get.call_count == 3
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"deductible": 1000, "stop_loss": 10000, "oop_max": 5000}


def test_index_max_coalesce_strategy():
    with patch('app.main.http_get') as mock_http_get:
        mock_http_get.side_effect = [
            {"deductible": 1000, "stop_loss": 10000, "oop_max": 5000},
            {"deductible": 1200, "stop_loss": 13000, "oop_max": 6000},
            {"deductible": 1000, "stop_loss": 10000, "oop_max": 6000},
        ]

        response = client.get("/?member_id=1000&strategy=max")

        assert mock_http_get.call_count == 3
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"deductible": 1200, "stop_loss": 13000, "oop_max": 6000}
