import json
from flask import Flask, render_template, request, redirect, flash, url_for
from datetime import datetime

MAX_BOOKING = 12

class BookingError(Exception):
    pass

class InvalidInputError(Exception):
    pass

class ClubPointsError(Exception):
    pass

class CompetitionPlacesError(Exception):
    pass

class MaxBookingError(Exception):
    pass

class DateError(Exception):
    pass



def loadClubs(file_path="clubs.json"):
    with open(file_path) as c:
        listOfClubs = json.load(c)["clubs"]
        return listOfClubs


def loadCompetitions(file_path="competitions.json"):
    with open(file_path) as comps:
        listOfCompetitions = json.load(comps)["competitions"]
        return listOfCompetitions
    


app = Flask(__name__)
app.secret_key = "something_special"

competitions = loadCompetitions()
clubs = loadClubs()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/showSummary", methods=["POST"])
def showSummary():
    email = request.form["email"]
    try:
        club = [club for club in clubs if club["email"] == email][0]
            
    except IndexError:
        flash(f"Error: email {email} does not exist")
        return redirect(url_for("index"))
    
    return render_template("welcome.html", club=club, competitions=competitions, clubs=clubs)

def limit_max(club, competition):
    if int(club["points"]) >= int(competition["numberOfPlaces"]):
        points = int(competition["numberOfPlaces"])
    else:
        points = int(club["points"])
    if points < 12 :
        limit = points
    else:
        limit = 12
    return limit

@app.route("/book/<competition>/<club>")
def book(competition, club):
    foundClub = [c for c in clubs if c["name"] == club][0]
    foundCompetition = [c for c in competitions if c["name"] == competition][0]
    if foundClub and foundCompetition:
        limit = limit_max(foundClub, foundCompetition)
        return render_template(
            "booking.html", club=foundClub, competition=foundCompetition, limit=limit
        )
    else:
        flash("Something went wrong-please try again")
        return render_template("welcome.html", club=club, competitions=competitions)

def find_competition(competition_name, competitions):
    competition = [c for c in competitions if c["name"] == competition_name]
    if not competition:
        raise BookingError("Competition not found or invalid")
    return competition[0]

def find_club(club_name, clubs):
    club = [c for c in clubs if c["name"] == club_name]
    if not club:
        raise BookingError("Club not found or invalid")
    return club[0]

def validate_booking_input(place_required_str):
    if not place_required_str:
        raise InvalidInputError("Invalid number of places. Please enter a positive number only")

def validate_booking_number_input(place_required):
    if place_required <= 0:
        raise InvalidInputError("Invalid number of places. Please enter a positive number only")
    
def validate_points_club_available(club, place_required):
    if place_required > int(club["points"]):
        raise ClubPointsError("Not enought club points left")
    
def validate_competition_points_available(competition, place_required):
    if place_required > int(competition["numberOfPlaces"]):
        raise CompetitionPlacesError("Not enought competition places left")
    
def validate_book_12_max(place_required):
    if place_required > MAX_BOOKING:
        raise MaxBookingError("You can book 12 places maximum")
    
def validate_datetime(date):
    competition_date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    if competition_date <= datetime.now():
        raise DateError("You can't book places from a passed competition")

    
@app.route("/purchasePlaces", methods=["POST"])
def purchasePlaces():

    competition_name = request.form["competition"]  
    club_name = request.form["club"]
    place_required_str = request.form["places"]
    try:
        competition = find_competition(competition_name, competitions)
        club = find_club(club_name, clubs)
        date = competition["date"]
        

        validate_booking_input(place_required_str)
        
        place_required = int(request.form["places"])
        validate_datetime(date)
        validate_booking_number_input(place_required)
        validate_points_club_available(club, place_required)
        validate_competition_points_available(competition, place_required)
        validate_book_12_max(place_required)
        
        competition["numberOfPlaces"] = int(competition["numberOfPlaces"]) - place_required
        club["points"] = int(club["points"]) - place_required
        flash("Great-booking complete!")
        
    except DateError as e:
        flash(str(e))
        return redirect(url_for("book", competition=competition_name, club=club_name))
    
    except BookingError as e:
        flash(str(e))
        return redirect(url_for("book", competition=competition_name, club=club_name))
        
    except InvalidInputError as e:
        flash(str(e))
        return redirect(url_for("book", competition=competition_name, club=club_name))
        
    except ClubPointsError as e:
        flash(str(e))
        return redirect(url_for("book", competition=competition_name, club=club_name))
    
    except CompetitionPlacesError as e:
        flash(str(e))
        return redirect(url_for("book", competition=competition_name, club=club_name, limit=limit))
    
    except MaxBookingError as e:
        flash(str(e))
        return redirect(url_for("book", competition=competition_name, club=club_name, limit=limit))
        
    return render_template("welcome.html", club=club, competitions=competitions)


# TODO: Add route for points display


@app.route("/logout")
def logout():
    return redirect(url_for("index"))
