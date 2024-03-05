import pytest
from server import validate_competition_points_available, CompetitionPlacesError

def test_validate_competition_points_available_ok(new_competitions_fixture):
    competitions = new_competitions_fixture["competitions"]
    competition = competitions[0]
    place_required = 10
    
    response = validate_competition_points_available(competition, place_required)
    
    assert response == None
    
    
def test_validate_competition_points_available_error(new_competitions_fixture):
    competitions = new_competitions_fixture["competitions"]
    competition = competitions[2]
    place_required = 10
    
    with pytest.raises(CompetitionPlacesError):
        validate_competition_points_available(competition, place_required)