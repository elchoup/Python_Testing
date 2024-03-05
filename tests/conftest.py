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
def new_competitions_fixture():
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
                "date":"2024-12-25 13:30:00",
                "numberOfPlaces": "3"
            },
            {
                "name": "Competition 1",
                "date": "2024-11-18 13:30:00",
                "numberOfPlaces": "15"
            },
            {
                "name": "Competition 2",
                "date": "2024-10-12 13:30:00",
                "numberOfPlaces": "10"
            }
        ]
    }
    return competitions




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
            "date":"2024-12-25 14:00:00",
            "numberOfPlaces": "3"
            }
        ]
    }
    
    return competitions