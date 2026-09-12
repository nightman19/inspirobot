from .base import *
import os
import dj_database_url

DEBUG = False

SECRET_KEY = os.environ.get("SECRET_KEY")

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", ".onrender.com").split(",")

DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    raise Exception(
        "DATABASE_URL environment variable is not set."
        "Production requires a persistent Postgres database - see Render "
        "Environment settings."
    )

DATABASES = {
    "default": dj_database_url.parse(
        DATABASE_URL,
        conn_max_age=600,
        ssl_require=True
    )
}

# Security settings
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"