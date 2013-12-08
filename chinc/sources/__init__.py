import os.path
import pkgutil

SOURCES_PATH = os.path.dirname(__file__)


def find_sources():
    return [name for _, name, _ in pkgutil.iter_modules([SOURCES_PATH])]


def load_source(name, fromlist=None):
    return __import__(
        __package__+'.sources.'+name,
        fromlist = fromlist,
        level = 0)
