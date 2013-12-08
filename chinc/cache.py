from functools import wraps
import os
import os.path

from xdg.BaseDirectory import save_cache_path


def delay(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        return lambda: func(*args, **kwargs)

    return wrapper


def load_data(namespace, key, default):
    dirpath = save_cache_path(__package__, namespace)
    filename = os.path.join(dirpath, key)

    try:
        f = open(filename, 'r')
        with f:
            return f.read()
    except IOError:
        data = default()

        with open(filename+".temp", 'w') as f:
            f.write(data)

        os.rename(filename+".temp", filename)

        return data
