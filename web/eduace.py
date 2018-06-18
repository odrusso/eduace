"""
 ___   ___    _   _     _      ___   ___
| __| |   \  | | | |   /_\    / __| | __|
| _|  | |) | | |_| |  / _ \  | (__  | _|
|___| |___/   \___/  /_/ \_\  \___| |___|

Main Web App

Python 3.6.5
Written by Oscar Russo for EduAce NZ

"""

# Dependency  Imports
from flask import Flask, render_template, g, jsonify, request, redirect
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user
import sqlite3

# Internal Imports
from src.courses import course_master
from src.courses.ncea_level_1.maths import mcat
from data_abstract import *


app = Flask(__name__)
login_manager = LoginManager(app)

app.config["SECRET_KEY"] = "somebullshitsecretkey"

class User(UserMixin):
    def __init__(self, id):
        self.id = int(id)
        datauser = get_user_from_id(self.id)
        # user_db = sqlite3.connect('data/users.db')
        # database_user = user_db.cursor().execute("""SELECT * FROM `Users` WHERE `id`=?""", (id,)).fetchone()
        # user_db.close()
        print(datauser)
        self.username = datauser.username
        self.email = datauser.email
        self.role = datauser.role
        self.score = datauser.score

@login_manager.user_loader
def load_user(id):
        return User(id)

@app.route("/")
def web_index():
    return render_template("index.html")

@app.route("/login")
def web_login():
    if current_user.is_anonymous:
        return render_template("login.html", failure='None')
    else:
        return redirect('/dashboard')

@app.route('/login', methods=['POST'])
def verify_login():
    username = request.form['username']
    password = request.form['password']
    result = pull_user(username, password)
    if result[0]:
        user_id = result[1]
        login_user(load_user(user_id))
        return redirect("/dashboard")
    elif result[1] == 'username':
        return render_template("/login.html", failure="username")  # failure state required
    else:
        return render_template("/login.html", failure="password")  # failure state required


@app.route("/_logout")
@login_required
def user_logout():
    logout_user()
    return redirect("/")

@app.route("/dashboard")
@login_required
def web_dashboard():
    g.all_courses = course_master.get_list_of_courses()
    g.score = current_user.score
    return render_template('dashboard.html')

@app.route("/pre-quiz-browse")
@login_required
def web_pre_quiz_browse():
    return "None"

@app.route("/quiz")
@login_required
def web_quiz():

    return render_template("quiz.html")

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)