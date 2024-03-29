import os


API_VERSION = "/api/v1"

DEBUG = os.environ.get("FLASK_DEBUG", "False") == "True"
CORS_ALLOWED_ORIGINS = "http://localhost:8080" if DEBUG else "https://eduace.net"
PORT = int(os.environ.get("FLASK_PORT", 80))
GIT_HASH = os.environ.get("GIT_HASH_VERSION", "")
