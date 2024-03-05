import pytest
from server import app

@pytest.fixture
def client():
    return app.test_client()

def test_date_competition_passed(client, new_competitions_fixture, club_fixture, monkeypatch):
    monkeypatch.setattr("server.competitions", new_competitions_fixture["competitions"])
    monkeypatch.setattr("server.clubs", club_fixture["clubs"])
    
    competition_name = "Fall Classic"
    club_name = "She Lifts"
    place_required = 10
    
    response = client.post("/purchasePlaces", data={"competition": competition_name, "club": club_name, "places": place_required}, follow_redirects=True)
    print(response.data)
    
    assert b"You can&#39;t book places from a passed competition" in response.data