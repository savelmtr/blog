from .base import *


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': f'{os.environ.get("MEMCACHED_HOST", "127.0.0.1")}:{os.environ.get("MEMCACHED_PORT", "11211")}',
    }
}


try:
    from .local import *
except ImportError:
    pass
