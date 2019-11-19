def get_env(env_variable):
    try:
      	return os.environ[env_variable]
    except KeyError:
        error_msg = 'Missing environment variable {} '.format(var_name)
        raise ImproperlyConfigured(error_msg)