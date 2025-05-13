import os


def get_env_bool(key, default=False):
    val = os.environ.get(key, str(default)).lower()
    return val in ('1', 'true', 't', 'yes', 'y')