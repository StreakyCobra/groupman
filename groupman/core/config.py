# -*- coding: utf-8 -*-

import os
from collections import OrderedDict

# Default configuration values
defaults = OrderedDict()
defaults['EDITOR'] = os.environ.get('EDITOR', 'vim')
defaults['PACMAN'] = os.environ.get('PACMAN', 'pacman')
defaults['USE_SUDO'] = 'true' if defaults['PACMAN'] == 'pacman' else 'false'

# Set some paths
home_path     = os.environ.get('HOME')
xdg_path      = os.environ.get('XDG_CONFIG_HOME', os.path.join(home_path, '.config'))
groupman_path = os.path.join(xdg_path, 'groupman')
db_path       = os.path.join(groupman_path, 'db')
config_path   = os.path.join(groupman_path, 'config')
groups_path   = os.path.join(groupman_path, 'groups')


def _read_conf(filepath):
    """Read a configuration file."""
    # Read lines in the file
    with open(filepath, 'r') as f:
        lines = f.readlines()
    # Strip lines
    lines = map(lambda x: x.strip(), lines)
    # Remove comments
    lines = filter(lambda x: x[0] != '#', lines)
    lines = map(lambda x: x.split('#')[0], lines)
    # Split at equal sign
    lines = map(lambda x: x.split('='), lines)
    # Remove lines that have not exactly 2 values
    lines = filter(lambda x: len(x) == 2, lines)
    # Prepare to be transformed as a dict
    lines = map(lambda x: (x[0].strip(), x[1].strip()), lines)
    # Transform to dict
    vals = OrderedDict(lines)
    # Return configuration
    return vals


def _write_conf(vals, filepath):
    """Write the configuration file from the given configuration."""
    # Transform configuration to string lines
    lines = map(lambda x: "%s = %s\n" % (str(x[0]), str(x[1])), vals.items())
    # Write the lines
    with open(filepath, 'w') as f:
        f.writelines(lines)


# Ensure groupman config folder is existing
if not os.path.isdir(groupman_path):
    os.makedirs(groupman_path)

# Ensure database file is existing
if not os.path.isfile(db_path):
    with open(db_path, 'w') as f:
        f.write('')

# Ensure config file is existing
if not os.path.isfile(config_path):
    _write_conf(defaults, config_path)

# Ensure groups folder is existing
if not os.path.isdir(groups_path):
    os.makedirs(groups_path)

# Read the user configuration
user_conf = _read_conf(config_path)


def g(val):
    """Get a configuration value by its key.
    Return user defined value if existing, otherwise the defaults value. Raise
    an KeyError if the key is not existing in both.
    """
    # If the user has defined the value return it
    if val in user_conf:
        return user_conf[val]
    # If there is a default value return it
    elif val in defaults:
        return defaults[val]
    # Otherwise raise an exception
    else:
        raise KeyError('Configuration key not existing.')
