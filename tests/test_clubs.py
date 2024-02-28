from server import loadClubs
import pytest


def test_load_clubs_valid(club_fixture):
    # Test when list of clubs exists
    expected_clubs = club_fixture["clubs"]
    loaded_clubs = loadClubs()
    # Assert the response is as expected
    assert loaded_clubs == expected_clubs
    
def test_load_clubs_no_club():
    # Assert FileNotFoundError raises if the file path is not existing
    with pytest.raises(FileNotFoundError):
        loadClubs(file_path="no_file.json")
    
    
    
    
