from server import loadClubs
import pytest


    
def test_load_clubs_no_club():
    # Assert FileNotFoundError raises if the file path is not existing
    with pytest.raises(FileNotFoundError):
        loadClubs(file_path="no_file.json")
        
def test_load_clubs_valid():
    response = loadClubs()
    data = {
        "name":"Simply Lift",
        "email":"john@simplylift.co",
        "points":"13"
    }
    
    assert data in response
    assert len(response) == 3
    
    
    
    
