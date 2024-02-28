import pytest
import server
from server import app, showSummary
from bs4 import BeautifulSoup

@pytest.fixture
def client():
    return app.test_client()

def test_show_summary_wrong_email(client):
    # Test when no email is provided
    email = 'bad-mail@gmail.com'
    response = client.post("/showSummary", data={"email": email}, follow_redirects=True)
    assert b"Error: email" in response.data
    assert b"does not exist" in response.data
    
    
def test_show_summary_valid_email(client):
    # Test when email is valid
    email = "john@simplylift.co"
    response = client.post("/showSummary", data={"email": email})
    # Assert the response status code is (OK)
    assert response.status_code == 200
    # Parse the html to catch the <h2>
    soup = BeautifulSoup(response.data, "html.parser")
    h2_tag = soup.find("h2")
    # Assert h2 exists
    assert h2_tag is not None
    h2_text = h2_tag.text.strip()
    expeted_text = f"Welcome, {email}"
    # Assert h2 text is the same as the expected one
    assert expeted_text == h2_text
