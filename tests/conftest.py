import pytest

@pytest.fixture
def club_fixture():
    clubs ={"clubs":
        [
        {
        "name":"Simply Lift",
        "email":"john@simplylift.co",
        "points":"13"
        },
        {
            "name":"Iron Temple",
            "email": "admin@irontemple.com",
            "points":"4"
        },
        {   "name":"She Lifts",
            "email": "kate@shelifts.co.uk",
            "points":"13"
        }
        ]
    }
    return clubs



@pytest.fixture
def competitions_fixture():
    competitions = {
        "competitions": [
            {
                "name": "Spring Festival",
                "date": "2020-03-27 10:00:00",
                "numberOfPlaces": "25"
            },
            {
                "name": "Fall Classic",
                "date": "2020-10-22 13:30:00",
                "numberOfPlaces": "13"
            },
            {
            "name": "Test",
            "date":"2024-12-25",
            "numberOfPlaces": "3"
            }
        ]
    }
    
    return competitions