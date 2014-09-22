from configparser import RawConfigParser as ConfigParser, NoSectionError, NoOptionError
import glob
OPTIONS = None
CONFIG_DIR = '/etc/webtoys/*.conf'
def get_options():
    global OPTIONS
    if OPTIONS is None:
        OPTIONS = ConfigParser()
        OPTIONS.read( sorted(glob.glob(CONFIG_DIR)))
    return OPTIONS

def get_boolean(section,key, default=None):
    try:
        return get_options().getboolean(section,key)
    except (NoSectionError,NoOptionError) as err:
        return default 
def get_string(section,key, default=None):
    try:
        return get_options().get(section,key)
    except (NoSectionError,NoOptionError) as err:
        return default 
def get_float(section,key, default=None):
    try:
        return get_options().getfloat(section,key)
    except (NoSectionError,NoOptionError) as err:
        return default 
def get_integer(section,key, default=None):
    try:
        return get_options().getinteger(section,key)
    except (NoSectionError,NoOptionError) as err:
        return default 


