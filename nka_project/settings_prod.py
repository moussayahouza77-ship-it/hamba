from .settings import *
import os
from pathlib import Path

# Load .env if present (for local testing)
from dotenv import load_dotenv
env_path = Path(BASE_DIR) / '.env'
load_dotenv(dotenv_path=env_path)

# Production overrides
DEBUG = os.environ.get('DJANGO_DEBUG', 'False') == 'True'

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', SECRET_KEY)

ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', '').split(',') if os.environ.get('DJANGO_ALLOWED_HOSTS') else ['yourdomain.com']

# Use WhiteNoise to serve static files in production
MIDDLEWARE = ['whitenoise.middleware.WhiteNoiseMiddleware'] + MIDDLEWARE

STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Security settings
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = os.environ.get('DJANGO_SECURE_SSL_REDIRECT', 'True') == 'True'
SECURE_HSTS_SECONDS = int(os.environ.get('DJANGO_SECURE_HSTS_SECONDS', 3600))
SECURE_HSTS_INCLUDE_SUBDOMAINS = os.environ.get('DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS', 'True') == 'True'
SECURE_HSTS_PRELOAD = os.environ.get('DJANGO_SECURE_HSTS_PRELOAD', 'True') == 'True'
X_FRAME_OPTIONS = os.environ.get('DJANGO_X_FRAME_OPTIONS', 'DENY')

# Database configuration: prefer DATABASE_URL (Postgres), else keep default sqlite
import dj_database_url
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL:
	DATABASES = {
		'default': dj_database_url.parse(DATABASE_URL, conn_max_age=600)
	}
