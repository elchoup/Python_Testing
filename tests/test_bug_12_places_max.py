import pytest
from server import app


@pytest.fixture
def client():
    return app.test_client()

def test_book_less_max_booking(client, new_competitions_fixture, club_fixture, monkeypatch):
    monkeypatch.setattr("server.competitions", new_competitions_fixture["competitions"])
    monkeypatch.setattr("server.clubs", club_fixture["clubs"])
    
    competition_name = "Competition 1"
    club_name = "Simply Lift"
    place_required = 10
    
    response = client.post("/purchasePlaces", data={"competition": competition_name, "club": club_name, "places": place_required}, follow_redirects=True)
    
    assert response.status_code == 200
    assert b"Great-booking complete!" in response.data
    
    
def test_book_more_max_booking(client, new_competitions_fixture, club_fixture, monkeypatch):
    monkeypatch.setattr("server.competitions", new_competitions_fixture["competitions"])
    monkeypatch.setattr("server.clubs", club_fixture["clubs"])
    
    competition_name = "Competition 1"
    club_name = "She Lifts"
    place_required = 13
    
    response = client.post("/purchasePlaces", data={"competition": competition_name, "club": club_name, "places": place_required}, follow_redirects=True)
    print(response.data)
    
    assert b"You can book 12 places maximum" in response.data
    

