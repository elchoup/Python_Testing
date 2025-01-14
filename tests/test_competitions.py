from server import loadCompetitions
import pytest

"""def test_load_competitions_valid(competitions_fixture):
    # Test when list of competitions exists
    expected_competitions = competitions_fixture["competitions"]
    loaded_competitions = loadCompetitions()
    # Assert the response is as expected
    assert loaded_competitions == expected_competitions"""
    
def test_load_compettions_empty():
    # Assert FileNotFoundError raises if the file path is not existing
    with pytest.raises(FileNotFoundError):
        loadCompetitions(file_path="no_file.json")
        
def test_load_competition_valid_1():
    response = loadCompetitions()
    data = {
            "name": "Spring Festival",
            "date": "2020-03-27 10:00:00",
            "numberOfPlaces": "25"
        }
    
    assert data in response
    assert len(response) == 4