import os


API_VERSION = "/api/v1"

DEBUG = os.environ.get("FLASK_DEBUG", "False") == "True"
CORS_ALLOWED_ORIGINS = "https://localhost:5000" if DEBUG else ""
