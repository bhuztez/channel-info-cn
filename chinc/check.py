from .sources import find_sources, load_source


def check_channel_info(name):
    mod = load_source(name, ['check_channel_info'])
    return mod.check_channel_info()
