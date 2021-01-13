from .base import *


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': f'{os.environ.get("MEMCACHED_HOST", "127.0.0.1")}:{os.environ.get("MEMCACHED_PORT", "11211")}',
    }
}

EMAIL_HOST = os.environ.get("EMAIL_HOST")
EMAIL_PORT = int(os.environ.get("EMAIL_PORT", default=25))
EMAIL_USE_TLS = True

try:
    from .local import *
except ImportError:
    pass
