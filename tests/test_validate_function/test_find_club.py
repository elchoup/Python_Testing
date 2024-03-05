import pytest
from server import find_club, BookingError

def test_find_club_ok(club_fixture):
    clubs = club_fixture["clubs"]
    club = clubs[0]
    club_name = club["name"]
    
    response = find_club(club_name, clubs)
    
    assert response == club
    
    
def test_find_club_error(club_fixture):
    clubs = club_fixture["clubs"]
    club_name = "Wrong Name"
    
    with pytest.raises(BookingError):
        find_club(club_name, clubs)