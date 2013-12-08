from urllib import urlopen, urlencode
import json

from ..cache import delay, load_data
from ..info import get_channel, get_streams, Channel
from ..result import NOT_CHANGED, CHANGED, NEW, MISSING

namespace = __name__.rsplit('.', 1)[-1]


@delay
def fetch_channel_info(channels):
    url = 'http://tv.cntv.cn/api/epg/now'
    params = urlencode({'cb': '', 'c': ','.join(channels)})

    response = urlopen(url+'?'+params)
    return response.read()


def check_channel_info():
    streams = get_streams(namespace)
    s = {v:k for k,v in streams.items()}

    data = load_data(
        namespace,
        "channels",
        fetch_channel_info(streams.values()))

    results = []

    for c in json.loads(data):
        channel = get_channel(s.pop(c["c"], None))

        if channel is None:
            yield (NEW, c)
        elif channel.name == c["n"].encode('utf-8'):
            yield (NOT_CHANGED, channel)
        else:
            yield (CHANGED, channel, c)

    for c in s.values():
        yield (MISSING, get_channel(c))
