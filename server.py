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
    """ 
    Function to load the clubs in the json file

    """
    with open(file_path) as c:
        listOfClubs = json.load(c)["clubs"]
        return listOfClubs


def loadCompetitions(file_path="competitions.json"):
    """ 
    Function to load the competitions in the json file

    """
    with open(file_path) as comps:
        listOfCompetitions = json.load(comps)["competitions"]
        return listOfCompetitions
    


app = Flask(__name__)
app.secret_key = "something_special"

competitions = loadCompetitions()
clubs = loadClubs()

def limit_max(club, competition):
    """
    Function to calculate the limit max of booking available
    making a calculation between the club points left, the competition points
    left and the limit of 12 booking max

    """
    if int(club["points"]) >= int(competition["numberOfPlaces"]):
        points = int(competition["numberOfPlaces"])
    else:
        points = int(club["points"])
    if points < 12 :
        limit = points
    else:
        limit = 12
    return limit

def find_competition(competition_name, competitions):
    """
    Function to find the competition in the list or raise an error
    
    """
    competition = [c for c in competitions if c["name"] == competition_name]
    if not competition:
        raise BookingError("Competition not found or invalid")
    return competition[0]

def find_club(club_name, clubs):
    """
    Function to find the club in the list or raise an error
    
    """
    club = [c for c in clubs if c["name"] == club_name]
    if not club:
        raise BookingError("Club not found or invalid")
    return club[0]

def validate_booking_input(place_required_str):
    """
    Function to raise an error if the place_required input is sent empty
    
    """
    if not place_required_str:
        raise InvalidInputError("Invalid number of places. Please enter a positive number only")

def validate_booking_number_input(place_required):
    """
    Function to make sure the place_required input is higher than 0
    
    """
    if place_required <= 0:
        raise InvalidInputError("Invalid number of places. Please enter a positive number only")
    
def validate_points_club_available(club, place_required):
    """
    Function to check if club have enought places left
    
    """
    if place_required > int(club["points"]):
        raise ClubPointsError("Not enought club points left")
    
def validate_competition_points_available(competition, place_required):
    """
    Function to check if competition have enought places left
    
    """
    if place_required > int(competition["numberOfPlaces"]):
        raise CompetitionPlacesError("Not enought competition places left")
    
def validate_book_12_max(place_required):
    """
    Function to check if the user isn't asking more places than the max limit
    
    """
    if place_required > MAX_BOOKING:
        raise MaxBookingError("You can book 12 places maximum")
    
def validate_datetime(date):
    """
    Function to check if the date of the competition is not passed
    
    """
    competition_date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    if competition_date <= datetime.now():
        raise DateError("You can't book places from a passed competition")
    
def purchase_validation(date, place_required, club, competition):
    """
    Function using all the validation function like a isValid function
    
    """
    validate_datetime(date)
    validate_booking_number_input(place_required)
    validate_points_club_available(club, place_required)
    validate_competition_points_available(competition, place_required)
    validate_book_12_max(place_required)
    
@app.context_processor
def inject_datetime():
    """
    Function to inject datetime in the html files
    
    """
    return dict(datetime=datetime)



@app.route("/")
def index():
    return render_template("index.html", clubs=clubs)


@app.route("/showSummary", methods=["POST"])
def showSummary():
    """
    Function to catch a email request and check if the email is one of the club list
    If it is redirect to the welcome page or send an error
    
    """
    email = request.form["email"]
    try:
        club = [club for club in clubs if club["email"] == email][0]
            
    except IndexError:
        flash(f"Error: email {email} does not exist")
        return redirect(url_for("index"))
    
    
    return render_template("welcome.html", club=club, competitions=competitions, clubs=clubs)


@app.route("/book/<competition>/<club>")
def book(competition, club):
    """
    Function to send to purchase places page checking if 
    club and competition selected are in the list
    Create a max limit with the limit_max function
    
    """
    try:
        foundClub = [c for c in clubs if c["name"] == club][0]
        foundCompetition = [c for c in competitions if c["name"] == competition][0]
    except IndexError:
        flash(f"Error: Not found in list")
        return redirect(url_for("index"))
    
    if foundClub and foundCompetition:
        limit = limit_max(foundClub, foundCompetition)
        return render_template(
            "booking.html", club=foundClub, competition=foundCompetition, limit=limit
        )
    else:
        flash("Something went wrong-please try again")
        return render_template("welcome.html", club=club, competitions=competitions, clubs=clubs)

    
@app.route("/purchasePlaces", methods=["POST"])
def purchasePlaces():
    """
    Function to purchase places using competition, club and places request
    Use the isValid function to catch all the errors possible and 
    send back to the welcome page with a success message
    
    """
    competition_name = request.form["competition"]  
    club_name = request.form["club"]
    place_required_str = request.form["places"]
    try:
        competition = find_competition(competition_name, competitions)
        club = find_club(club_name, clubs)
        date = competition["date"]
        

        validate_booking_input(place_required_str)
        
        place_required = int(request.form["places"])
        
        purchase_validation(date, place_required, club, competition)
        
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
        return redirect(url_for("book", competition=competition_name, club=club_name))
    
    except MaxBookingError as e:
        flash(str(e))
        return redirect(url_for("book", competition=competition_name, club=club_name))
        
    return render_template("welcome.html", club=club, competitions=competitions, clubs=clubs)


@app.route("/logout")
def logout():
    """
    Function to logout
    
    """
    return redirect(url_for("index"))
