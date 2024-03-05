import pytest
from server import validate_datetime, DateError

def test_validate_datetime_ok(new_competitions_fixture):
    competitions = new_competitions_fixture["competitions"]
    competition = competitions[3]
    competition_date = competition["date"]
    
    response = validate_datetime(competition_date)
    
    assert response == None
    
def test_validate_datetime_error(new_competitions_fixture):
    competitions = new_competitions_fixture["competitions"]
    competition = competitions[0]
    competition_date = competition["date"]
    
    with pytest.raises(DateError):
        validate_datetime(competition_date)