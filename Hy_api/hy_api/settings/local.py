from .base import *  
from .base import env

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="PwUYX5l39gVk7-myJr7Y9n9MvTPJzdgC9egosWocLTF7VC8kzao",
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True


EMAIL_BACKEND = "djcelery_email.backends.CeleryEmailBackend"
EMAIL_HOST = env("EMAIL_HOST", default="mailhog")
EMAIL_PORT = env("EMAIL_PORT")
DEFAULT_FROM_EMAIL = "henry_melen@hotmail.com"
DOMAIN = env("DOMAIN")
SITE_NAME = "Henry's Site"