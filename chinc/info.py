from ConfigParser import SafeConfigParser
from pkgutil import get_data

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

from .utils import NamedTuple


class Station(NamedTuple):
    __fields__ = ('id', 'name')


class Channel(NamedTuple):
    __fields__ = ('id', 'type', 'name', 'logo')


def read_info(name):
    data = get_data(__package__, "info/{name}.conf".format(name=name))
    parser = SafeConfigParser(allow_no_value=True)
    parser.readfp(StringIO(data))
    return parser


def load_info(name, type):
    parser = read_info(name)
    return [type(id=sec, **dict(parser.items(sec)))
            for sec in parser.sections()]


def load_channels(name):
    return load_info(name, Channel)


def load_stations():
    return load_info("stations", Station)


_stations = None
_channels = None
_streams = None

def load_all_channels():
    global _stations, _channels

    if _stations is not None:
        return

    _stations = {}
    _channels = {}

    stations = load_stations()

    for s in stations:
        channels = load_channels(s.id)
        _stations[s] = channels
        _channels.update((c.id, c) for c in channels)


def get_stations():
    global _stations
    load_all_channels()
    return _stations


def get_channel(name):
    global _channels
    load_all_channels()
    return _channels.get(name, None)


def get_streams(name):
    global _streams

    if _streams is None:
        parser = read_info("streams")
        _streams = dict((sec, dict(parser.items(sec))) for sec in parser.sections())

    return _streams.get(name, None)
