from decouple import config


DEBUG = config('DEBUG', cast=bool, default=False)
SECRET_KEY = config('SECRET_KEY', default="secret")
FLASK_ADMIN_SWATCH = 'darkly'
