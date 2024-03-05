import pytest
from server import validate_points_club_available, ClubPointsError

def test_validate_points_club_available_ok(club_fixture):
    clubs = club_fixture["clubs"]
    club = clubs[0]
    place_required = 10
    
    response = validate_points_club_available(club, place_required)
    
    assert response == None
    
def test_validate_points_club_available_error(club_fixture):
    clubs = club_fixture["clubs"]
    club = clubs[0]
    place_required = 15
    
    with pytest.raises(ClubPointsError):
        validate_points_club_available(club, place_required)