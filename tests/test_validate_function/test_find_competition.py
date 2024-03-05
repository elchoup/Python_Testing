import pytest
from server import find_competition, BookingError

def test_find_competition_ok(new_competitions_fixture):
    competitions = new_competitions_fixture["competitions"]
    competition = competitions[0]
    competition_name = competition["name"]
    
    response = find_competition(competition_name, competitions)
    print(response)
    
    assert response == competition
    
    
def test_find_competition_error(competitions_fixture):
    competitions = competitions_fixture["competitions"]
    competition_name = "Wrong Name"
    
    with pytest.raises(BookingError):
        find_competition(competition_name, competitions)