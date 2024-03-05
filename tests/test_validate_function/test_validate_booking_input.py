import pytest
from server import InvalidInputError, validate_booking_input

def test_validate_booking_input_error():
    place_required_str = ""
    with pytest.raises(InvalidInputError):
        validate_booking_input(place_required_str)