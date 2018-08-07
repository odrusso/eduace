import os

if os.getenv("DB_ENGINE") is None:
    DB_ENGINE = 'mysql+pymysql://eduace_db_admin:zg3-Ctg-dgP-2hU@eduace.csdwogwsprlc.ap-southeast-2.rds.amazonaws.com/eduace'
    DEBUG = True
else:
    DB_ENGINE = os.getenv("DB_ENGINE")
    DEBUG = False


# Development Variables
SECRET_KEY = "thequickbrownfoxjumpesoverthelazydog"
HOST = "0.0.0.0"
MAIL_SERVER = "smtp.mail.us-west-2.awsapps.com"
MAIL_USERNAME = "it@eduace.co.nz"
MAIL_PASSWORD = "3nK-6mG-5Le-SS8"
SENTRY_URL = 'https://ac173641bbe144a99d666c0dde8a388d:132651151e874f5981aaff223580ef34@sentry.io/1245240'
