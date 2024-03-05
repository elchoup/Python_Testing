import pytest
from server import validate_book_12_max, MaxBookingError

def test_validate_book_12_max_ok():
    place_required = 11
    
    response = validate_book_12_max(place_required)
    
    assert response == None
    
def test_validate_book_12_max_error():
    place_required = 13
    
    with pytest.raises(MaxBookingError):
        validate_book_12_max(place_required)