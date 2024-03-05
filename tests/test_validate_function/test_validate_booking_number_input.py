import pytest
from server import validate_booking_number_input, InvalidInputError

def test_validate_booking_number_input_ok():
    place_required = 10
    
    response = validate_booking_number_input(place_required)
    
    assert response == None
    
def test_validate_booking_number_input_error():
    place_required = -1
    
    with pytest.raises(InvalidInputError):
        validate_booking_number_input(place_required)