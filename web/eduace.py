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
from werkzeug.security import generate_password_hash
import pickle
import operator
import sys

# Internal Imports
sys.path.append('.')
sys.path.append('./enviroment/lib/python3.6/site-packages')

from src.courses import course_master
from src.courses.ncea_level_1.maths import mcat
from data_abstract import *
from generation import generate


app = Flask(__name__)
login_manager = LoginManager(app)

app.config["SECRET_KEY"] = "somebullshitsecretkey"

class User(UserMixin):
    def __init__(self, id):
        self.id = int(id)
        self.datauser = get_user_from_id(self.id)
        # user_db = sqlite3.connect('data/users.db')
        # database_user = user_db.cursor().execute("""SELECT * FROM `Users` WHERE `id`=?""", (id,)).fetchone()
        # user_db.close()
        self.username = self.datauser.username
        self.email = self.datauser.email
        self.role = self.datauser.role
        self.score = self.datauser.score
        self.current_structure = self.datauser.current_structure


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
    if current_user.current_structure == None:
        return render_template("dashboard_fresh.html")
    else:
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
    current_structure_object = current_user.datauser.question_structures.filter_by(question_structure_id=current_user.datauser.current_structure).first()
    current_question_list = current_structure_object.questions.all()
    quesiton_list = [[x.question_id, x.question_pointer] for x in current_question_list]
    sidebar_question_list = []
    for data_question_object in current_question_list:
        current = []
        current.append(data_question_object.question_id)
        current.append(data_question_object.question_structure_itt)
        current.append(data_question_object.question_pointer)
        current.append(data_question_object.get_question_status())
        sidebar_question_list.append(current)

    sidebar_question_list = sorted(sidebar_question_list, key=operator.itemgetter(1))

    return render_template("quiz.html", sidebar_question_list=sidebar_question_list, current_question=current_structure_object.current_question)


@app.route("/_load_question_json")
@login_required
def load_question_json():
    question_id = request.args.get("question_id")
    question = pickle.loads(session.query(DataQuestion).filter(DataQuestion.question_id == question_id).first().question_pickle)
    return jsonify(question_latex=question.question_aspects)


@app.route("/_evaluate_answer")
@login_required
def evaluate_answer():
    entered_answer = request.args.get("entered_latex")
    question_id = request.args.get("question_id")
    question = question = pickle.loads(session.query(DataQuestion).filter(DataQuestion.question_id == question_id).first().question_pickle)
    return jsonify(result=question.evaluate_answer(entered_answer))


@app.route("/register", methods=['GET', 'POST'])
def evaluagte_answer():
    if request.method == "POST":
        username_exists = len(session.query(DataUser.username).filter_by(username=request.form['username']).all()) != 0
        email_exists = len(session.query(DataUser.username).filter_by(email=request.form['email']).all()) != 0
        password = request.form['password']

        print(username_exists)

        if username_exists:
            print("user error")
            return render_template("register.html", error="Username already exists!")

        elif email_exists:
            print("email error")
            return render_template("register.html", error="Email already exists!")

        elif len(password) < 8:
            print("password error")
            return render_template("register.html", error="Password must be greater than 8 characters!")

        else:
            new_user = DataUser(username=request.form['username'], passhash=generate_password_hash(password), email=request.form["email"], role="demo", score=0)
            session.add(new_user)
            session.commit()
            print("sucess - user added")
            return render_template("register_success.html")
    else:
        if not current_user.is_anonymous:
            return redirect('/dashboard')
        else:
            return render_template("register.html", error="")
        print("initial render")


@app.route("/_generate_mcat_exam")
def generate_demo_exam():
    generate(current_user.id)
    return redirect('/dashboard')


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)