# kitab_backend/settings/heroku.py
import os
from .base import *  # Base settings-i import edin

# Heroku-specific settings
DEBUG = os.environ.get("DEBUG", "False") == "True"
SECRET_KEY = os.environ.get("SECRET_KEY", "django-insecure-default-secret-key")

# Database (Heroku DATABASE_URL)
DATABASES = {
    "default": dj_database_url.config(
        default=os.environ.get("DATABASE_URL")
    )
}

# Allowed Hosts
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")

# CORS
CORS_ALLOWED_ORIGINS = os.environ.get("CORS_ALLOWED_ORIGINS", "").split(",") if os.environ.get("CORS_ALLOWED_ORIGINS") else []

# Static files
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# WhiteNoise configuration for Heroku
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Redis Cache Configuration with Fallback
REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379')

# Redis URL-i SSL olmadan istifadə et
if REDIS_URL.startswith('rediss://'):
    REDIS_URL = REDIS_URL.replace('rediss://', 'redis://')

# Redis problemi olduqda avtomatik fallback
REDIS_ENABLED = os.environ.get('REDIS_ENABLED', 'True') == 'True'

if REDIS_ENABLED:
    try:
        # Redis cache konfiqurasiyası - connection pool problemi üçün
        CACHES = {
            'default': {
                'BACKEND': 'django_redis.cache.RedisCache',
                'LOCATION': REDIS_URL,
                'OPTIONS': {
                    'CLIENT_CLASS': 'django_redis.client.DefaultClient',
                    'CONNECTION_POOL_KWARGS': {
                        'max_connections': 10,  # Azaltdım
                        'retry_on_timeout': True,
                        'retry_on_error': True,
                        'socket_keepalive': True,
                        'socket_keepalive_options': {
                            'TCP_KEEPIDLE': 60,
                            'TCP_KEEPINTVL': 30,
                            'TCP_KEEPCNT': 3,
                        },
                    },
                    'SOCKET_CONNECT_TIMEOUT': 10,  # Artırdım
                    'SOCKET_TIMEOUT': 10,  # Artırdım
                    'RETRY_ON_TIMEOUT': True,
                    'IGNORE_EXCEPTIONS': True,  # Xətaları ignore et
                    # SSL problemi üçün - tamamilə deaktiv
                    'SSL': False,  # SSL deaktiv et
                    'SSL_CERT_REQS': None,
                    'SSL_CA_CERTS': None,
                    'SSL_CHECK_HOSTNAME': False,
                    'SSL_VERIFY_MODE': None,
                },
                'KEY_PREFIX': 'kitab_cache',
                'TIMEOUT': 300,  # 5 dəqiqə default timeout
            }
        }
        
        # Cache middleware
        MIDDLEWARE = [
            'django.middleware.cache.UpdateCacheMiddleware',  # Cache response
            *MIDDLEWARE,
            'django.middleware.cache.FetchFromCacheMiddleware',  # Cache request
        ]
        
        # Cache settings
        CACHE_MIDDLEWARE_SECONDS = 300  # 5 dəqiqə
        CACHE_MIDDLEWARE_KEY_PREFIX = 'kitab_middleware'
        CACHE_MIDDLEWARE_ALIAS = 'default'
        
        print("Redis cache aktiv edildi")
        
    except Exception as e:
        print(f"Redis cache konfiqurasiyası uğursuz oldu: {e}")
        print("Fallback local memory cache istifadə olunur...")
        REDIS_ENABLED = False

if not REDIS_ENABLED:
    # Fallback local memory cache
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'unique-snowflake',
            'TIMEOUT': 300,
        }
    }
    
    # Cache middleware deaktiv et
    MIDDLEWARE = MIDDLEWARE
    
    print("Local memory cache aktiv edildi")

# Email
EMAIL_HOST = os.environ.get("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.environ.get("EMAIL_PORT", 587))
EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS", "True") == "True"
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", EMAIL_HOST_USER)
ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", EMAIL_HOST_USER)

# ImageKit configuration is now imported from base.py
# No need to duplicate here

# Logging
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")