from decouple import config


DEBUG = config("DEBUG", cast=bool, default=False)
SECRET_KEY = config("SECRET_KEY", default="secret")
TOKEN = config("TOKEN", default=None)
FLASK_ADMIN_SWATCH = "darkly"
