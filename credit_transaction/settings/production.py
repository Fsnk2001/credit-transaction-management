from .base import *

# region GENERAL ---------------------------------------------------------------

DEBUG = False

# endregion --------------------------------------------------------------------

# region SECURITY -------------------------------------------------------

# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# SECURE_SSL_REDIRECT = True
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_NAME = '__Secure-csrftoken'
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_NAME = '__Secure-sessionid'
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# endregion --------------------------------------------------------------------

# region LOGGING ---------------------------------------------------------------

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': './django_errors.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}

# endregion --------------------------------------------------------------------
