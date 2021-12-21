import os


API_VERSION = "/api/v1"

DEBUG = os.environ.get("FLASK_DEBUG", "False") == "True"
CORS_ALLOWED_ORIGINS = "http://localhost:8080" if DEBUG else ""
