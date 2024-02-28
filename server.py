import json
from flask import Flask, render_template, request, redirect, flash, url_for

MAX_BOOKING = 12

class BookingError(Exception):
    pass

class InvalidInputError(Exception):
    pass

class ClubPointsError(Exception):
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
    
    return render_template("welcome.html", club=club, competitions=competitions)


@app.route("/book/<competition>/<club>")
def book(competition, club):
    foundClub = [c for c in clubs if c["name"] == club][0]
    foundCompetition = [c for c in competitions if c["name"] == competition][0]
    if foundClub and foundCompetition:
        return render_template(
            "booking.html", club=foundClub, competition=foundCompetition
        )
    else:
        flash("Something went wrong-please try again")
        return render_template("welcome.html", club=club, competitions=competitions)

def find_competition(competition_name):
    competition = [c for c in competitions if c["name"] == competition_name][0]
    if not competition:
        raise BookingError("Competition not found or invalid")
    return competition

def find_club(club_name):
    club = [c for c in clubs if c["name"] == club_name][0]
    if not club:
        raise BookingError("Club not found or invalid")
    return club

def validate_booking_input(place_required_str):
    if not place_required_str:
        raise InvalidInputError("Invalid number of places. Please enter a positive number only")

def validate_booking_number_input(place_required):
    if place_required <= 0:
        raise InvalidInputError("Invalid number of places. Please enter a positive number only")
    
def validate_points_club_available(club, place_required):
    if place_required > int(club["points"]):
        raise ClubPointsError("Not enought club points left")
    
@app.route("/purchasePlaces", methods=["POST"])
def purchasePlaces():
    try:
        competition_name = request.form["competition"]  
        club_name = request.form["club"]
        place_required_str = request.form["places"]
        
        competition = find_competition(competition_name)
        club = find_club(club_name)
        
        validate_booking_input(place_required_str)
        
        place_required = int(request.form["places"])
        
        validate_booking_number_input(place_required)
        validate_points_club_available(club, place_required)
        
        competition["numberOfPlaces"] = int(competition["numberOfPlaces"]) - place_required
        club["points"] = int(club["points"]) - place_required
        flash("Great-booking complete!")
    
    except BookingError as e:
        flash(str(e))
        return redirect(url_for("book", competition=competition_name, club=club_name))
        
    except InvalidInputError as e:
        flash(str(e))
        return redirect(url_for("book", competition=competition_name, club=club_name))
        
    except ClubPointsError as e:
        flash(str(e))
        return redirect(url_for("book", competition=competition_name, club=club_name))
        
    return render_template("welcome.html", club=club, competitions=competitions)


# TODO: Add route for points display


@app.route("/logout")
def logout():
    return redirect(url_for("index"))
