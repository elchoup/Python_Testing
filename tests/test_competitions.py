from server import loadCompetitions
import pytest

def test_load_competitions_valid(competitions_fixture):
    # Test when list of competitions exists
    expected_competitions = competitions_fixture["competitions"]
    loaded_competions = loadCompetitions()
    # Assert the response is as expected
    assert loaded_competions == expected_competitions
    
def test_load_compettions_empty():
    # Assert FileNotFoundError raises if the file path is not existing
    with pytest.raises(FileNotFoundError):
        loadCompetitions(file_path="no_file.json")