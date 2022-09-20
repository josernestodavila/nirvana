import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_api_one():
    response = client.get("/api_one?member_id=1000")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"deductible": 1000, "stop_loss": 10000, "oop_max": 5000}


def test_api_two():
    response = client.get("/api_two?member_id=1000")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"deductible": 1200, "stop_loss": 13000, "oop_max": 6000}


def test_api_three():
    response = client.get("/api_three?member_id=1000")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"deductible": 1000, "stop_loss": 10000, "oop_max": 6000}


@pytest.mark.asyncio
def test_index():
    response = client.get("/?member_id=1000")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"deductible": 1066, "stop_loss": 11000, "oop_max": 5666}


def test_index_no_member_id():
    response = client.get("/")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
def test_index_min_coalesce_strategy():
    response = client.get("/?member_id=1000&strategy=min")
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
def test_index_max_coalesce_strategy():
    response = client.get("/?member_id=1000&strategy=max")
    assert response.status_code == status.HTTP_200_OK
