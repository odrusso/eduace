# External Imports
from sqlalchemy import create_engine, Column, ForeignKey, INTEGER, String, BLOB, FLOAT, Boolean
from sqlalchemy.exc import InternalError, StatementError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from werkzeug.security import generate_password_hash, check_password_hash
import pickle


Base = declarative_base()

def pull_user(username, password):
    """Returns [True, UserID] if the user exists, and the password is correct,
    returns [False, "username] if the user does not exist, and
    returns [False, "password"] if the user exists, but the password is incorrect"""
    user_result = session.query(DataUser).filter(DataUser.username==username).all()
    if len(user_result) == 0:
        return [False, "username"]
    else:
        current_user = user_result[0]
        if check_password_hash(current_user.passhash, password):
            return [True, current_user.user_id]
        else:
            return [False, "password"]

def get_user_from_id(id):
    try:
        return session.query(DataUser).filter(DataUser.user_id==id).first()
    except InternalError:
        session.rollback()
        get_user_from_id(id)
    except StatementError:
        session.rollback()
        get_user_from_id(id)



class DataUser(Base):
    __tablename__ = 'users'

    user_id = Column(INTEGER, primary_key=True)
    username = Column(String)
    email = Column(String)
    passhash = Column(String)
    role = Column(String)
    score = Column(INTEGER)
    current_structure = Column(INTEGER)

    question_structures = relationship("DataQuestionStructure", lazy='dynamic')

    def __repr__(self):
        return "<User(user_id='%s', username='%s', email='%s', role='%s', score='%s')>" % (
            self.user_id, self.username, self.email, self.role, self.score)

    def __str__(self):
        return "%s: %s" % (self.user_id, self.username)


class DataQuestionStructure(Base):
    __tablename__ = 'question_structure'

    question_structure_id = Column(INTEGER, primary_key=True)
    user_id = Column(INTEGER, ForeignKey('users.user_id'))
    time_generated = Column(FLOAT)
    time_completed = Column(FLOAT)
    current_question = Column(INTEGER)
    length = Column(INTEGER)

    questions = relationship("DataQuestion", lazy='dynamic')

    def __repr__(self):
        return "<QuestionStructure(id='%s', length='%s')>" % (
            self.question_structure_id, self.length)

    # MAKE ITTERATIABLE


class DataQuestion(Base):
    __tablename__ = 'questions'

    question_id = Column(INTEGER, primary_key=True)
    question_structure_id = Column(INTEGER, ForeignKey('question_structure.question_structure_id'))
    question_structure_itt = Column(INTEGER)
    question_pointer = Column(String)
    question_pickle = Column(BLOB)
    time_gen = Column(INTEGER)
    time_init = Column(FLOAT)
    time_completed = Column(FLOAT)
    current_timer = Column(INTEGER)

    answers = relationship("DataAnswer", lazy='dynamic')

    def get_question_status(self):
        if len(self.answers.all()) == 0:
            return "unanswered"
        elif self.time_completed != 0.0:
            return "correct"
        else:
            return "incorrect"

    def __repr__(self):
        return "<Question(id='%s')>" % self.question_id


class DataAnswer(Base):
    __tablename__ = 'answers'

    answer_id = Column(INTEGER, primary_key=True)
    question_id = Column(INTEGER, ForeignKey('questions.question_id'))
    answer_pickle = Column(BLOB)
    time_entered = Column(FLOAT)
    timer_current = Column(INTEGER)
    correct = Column(Boolean)

    def __repr__(self):
        return "<Answer(id='%s', completion='%s')>" % (self.answer_id, self.correct)


engine = create_engine(
    'mysql+pymysql://eduace_db_admin:zg3-Ctg-dgP-2hU@eduace.csdwogwsprlc.ap-southeast-2.rds.amazonaws.com/eduace')
print(__name__ + ": Engine Created")

Base.metadata.bind = engine
print(__name__ + ": Engine Bound to Base")


DBSession = sessionmaker(bind=engine)
print(__name__ + ": Engine Bound to Session")

session = DBSession()
print(__name__ + ": Session Initialised")

if __name__ == "__main__":
    test_user = session.query(DataUser).filter(DataUser.username == "oscar").one()
    print(test_user)
    print(test_user.question_structures.filter_by(question_structure_8id=test_user.current_structure).first())

    from src.courses.ncea_level_1.maths.mcat import *
    entered_question = pickle.dumps(MathsQuestion("1.1.1"))
    q = DataQuestion(question_structure_id=1, question_structure_itt=0, question_pointer='ncea_level_1.maths.mcat.Question("1.1.1")',
                 question_pickle=entered_question, time_init=0, time_completed=21345, current_timer=0)
    session.add(q)
    session.commit()

    question_data_testing = test_user.question_structures.first().questions.all()
    print(question_data_testing)
    question_testing = pickle.loads(question_data_testing[-1].question_pickle)
    print(question_testing.question_raw)