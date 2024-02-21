import json
from flask import Flask, render_template, request, redirect, flash, url_for


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
    email = request.form.get("email")
    try:
        club = next((club for club in clubs if club["email"] == email), None)
        if club:
            response = render_template("welcome.html", club=club, competitions=competitions)
            print(response)
            return response
        else:
            print("L'adresse email ne correspond à aucun club")
            return "L'adresse email ne correspond à aucun club"
            
    except IndexError:
        print("La liste des clubs est vide")
        return "La liste des clubs est vide"
    
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")
        return "Une erreur s'est produite"
        


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


@app.route("/purchasePlaces", methods=["POST"])
def purchasePlaces():
    competition = [c for c in competitions if c["name"] == request.form["competition"]][
        0
    ]
    club = [c for c in clubs if c["name"] == request.form["club"]][0]
    placesRequired = int(request.form["places"])
    competition["numberOfPlaces"] = int(competition["numberOfPlaces"]) - placesRequired
    flash("Great-booking complete!")
    return render_template("welcome.html", club=club, competitions=competitions)


# TODO: Add route for points display


@app.route("/logout")
def logout():
    return redirect(url_for("index"))
