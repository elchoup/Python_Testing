import pytest
from server import app
from flask import url_for

@pytest.fixture
def client():
    return app.test_client()

def test_logout(client):
    with app.test_request_context():
        response = client.get('/logout')
        assert response.status_code == 302
        assert response.headers['Location'] == url_for('index')
