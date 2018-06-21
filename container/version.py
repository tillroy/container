from pkgutil import get_data


def get_version():
    return get_data(__package__, 'VERSION').decode('utf8')