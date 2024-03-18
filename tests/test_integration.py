import pytest
from server import app, book

@pytest.fixture
def client():
    return app.test_client()

def test_all_application(client):
    email = "john@simplylift.co"
    response = client.post("/showSummary", data={"email": email})
    
    assert b"Welcome, john@simplylift.co" in response.data
    
    
    booking = client.get("/book/Test%202/Simply%20Lift")
    
    assert b"Booking for Test 2" in booking.data
    
    competition_name = "Test 2"
    
    club_name = "Simply Lift"
    
    place_required = 5
    
    purchase = client.post("/purchasePlaces", data={"competition":competition_name, "club":club_name, "places":place_required})
    
    assert b"Great-booking complete!" in purchase.data