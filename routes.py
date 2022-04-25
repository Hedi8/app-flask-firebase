import pyrebase
from flask import render_template, request, redirect, session
from app import app
import os

config = {
    "apiKey": "AIzaSyDc1AW03L71zvUZ2-Ka15S_B9X5mMX5fII",
    "authDomain": "farme-ca685.firebaseapp.com",
    "databaseURL": "https://farme-ca685-default-rtdb.europe-west1.firebasedatabase.app",
    "projectId": "farme-ca685",
    "storageBucket": "farme-ca685.appspot.com",
    "messagingSenderId": "683038567999",
    "appId": "1:683038567999:web:3816116b403daf5585128a",
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()
storage = firebase.storage()

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    if (request.method == 'POST'):
            email = request.form['name']
            password = request.form['password']
            try:
                auth.sign_in_with_email_and_password(email, password)
                #user_id = auth.get_account_info(user['idToken'])
                #session['usr'] = user_id
                return render_template('home.html')
            except:
                unsuccessful = 'Please check your credentials'
                return render_template('index.html', umessage=unsuccessful)
    return render_template('index.html')

@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if (request.method == 'POST'):
            email = request.form['name']
            password = request.form['password']
            auth.create_user_with_email_and_password(email, password)
            return render_template('index.html')
    return render_template('create_account.html')

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if (request.method == 'POST'):
            email = request.form['name']
            auth.send_password_reset_email(email)
            return render_template('index.html')
    return render_template('forgot_password.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    todo = db.child("vache").get()
    to = todo.val()
    return render_template('home.html', t=to.values())

@app.route('/photos/<filename>', methods=['GET', 'POST'])
def photo(filename):
    links = storage.child("vache/"+filename+".jpg").get_url(None)

    if request.method == "POST":

        # get the request data
        etat = request.form["etat"]
        ordonance = request.form["ordonance"]
        deplacement = request.form["deplacement"]
        traitement = {
            "etat": etat,
            "ordonance": ordonance,
            "deplacement":  deplacement,
            "num": filename
        }

        try:
            db.child("traitement").push(traitement)
            return redirect("/home")
        except:
            return render_template("photo.html", message="Something wrong happened")

    return render_template('photo.html', l=links)

@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        # get the request data
        num = request.form["num"]
        image = request.form["image"]
        vache = {
            "num": num,
            "image": image,
        }

        try:
            db.child("vachesain").push(vache)
            return redirect("/home")
        except:
            return render_template("create.html", message="Something wrong happened")

    return render_template("create.html")

@app.route("/about", methods=["GET", "POST"])
def aff():
    return render_template("aboutus.html")


if __name__ == '__main__':
    app.run()
