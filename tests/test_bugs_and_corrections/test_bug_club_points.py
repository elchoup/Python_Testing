import pytest
from server import app

@pytest.fixture
def client():
    return app.test_client()


def test_enough_club_points(client, new_competitions_fixture, club_fixture, monkeypatch):
    monkeypatch.setattr("server.competitions", new_competitions_fixture["competitions"])
    monkeypatch.setattr("server.clubs", club_fixture["clubs"])
    print(new_competitions_fixture)
    
    competition_name = "Competition 1"
    club_name = "Simply Lift"
    place_required = 10
    
    response = client.post("/purchasePlaces", data={"competition": competition_name, "club": club_name, "places": place_required}, follow_redirects=True)
    print(response.data)
    
    assert response.status_code == 200
    assert b"Great-booking complete!" in response.data
    
    
def test_not_enough_points(client, new_competitions_fixture, club_fixture, monkeypatch):
    monkeypatch.setattr("server.competitions", new_competitions_fixture["competitions"])
    monkeypatch.setattr("server.clubs", club_fixture["clubs"])
    
    
    competition_name = "Competition 1"
    club_name = "Iron Temple"
    place_required = 6
    
    response = client.post("/purchasePlaces", data={"competition": competition_name, "club": club_name, "places": place_required}, follow_redirects=True)
    print(response.data)
    
    assert b"Not enought club points left" in response.data
    
    
def test_input_empty(client, new_competitions_fixture, club_fixture, monkeypatch):
    monkeypatch.setattr("server.competitions", new_competitions_fixture["competitions"])
    monkeypatch.setattr("server.clubs", club_fixture["clubs"])
    
    competition_name = "Spring Festival"
    club_name = "Iron Temple"
    place_required = ""
    
    response = client.post("/purchasePlaces", data={"competition": competition_name, "club": club_name, "places": place_required}, follow_redirects=True)
    
    assert b"Invalid number of places. Please enter a positive number only" in response.data
    
    
def test_input_negative(client, new_competitions_fixture, club_fixture, monkeypatch):
    monkeypatch.setattr("server.competitions", new_competitions_fixture["competitions"])
    monkeypatch.setattr("server.clubs", club_fixture["clubs"])
    
    competition_name = "Competition 2"
    club_name = "Iron Temple"
    place_required = -2
    
    response = client.post("/purchasePlaces", data={"competition": competition_name, "club": club_name, "places": place_required}, follow_redirects=True)
    print(response.data)
    
    assert b"Invalid number of places. Please enter a positive number only" in response.data
    
    
    
    