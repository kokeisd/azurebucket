# Django dev environment settings

from .base import * 
from django.core.exceptions import ImproperlyConfigured

def get_env(env_variable):
    try:
      	return os.environ[env_variable]
    except KeyError:
        error_msg = 'Missing environment variable {} '.format(var_name)
        raise ImproperlyConfigured(error_msg)

DEBUG = True
ALLOWED_HOSTS = ['*']