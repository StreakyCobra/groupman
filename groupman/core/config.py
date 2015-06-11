# -*- coding: utf-8 -*-
"""Manage the configuration of groupman."""

import os
from collections import OrderedDict

# Configuration list separator
SEP = ','

# Default configuration values
defaults = OrderedDict()
defaults['EDITOR'] = os.environ.get('EDITOR', 'vim')
defaults['PACMAN_CMD'] = os.environ.get('PACMAN_CMD', 'pacman')
defaults['PACMAN_SUDO'] = 'true'
defaults['PACMAN_INSTALL'] = '-S' + SEP + '--needed'
defaults['PACMAN_REMOVE'] = '-Rs'
defaults['PACMAN_SET_EXP'] = '-D' + SEP + '--asexplicit'
defaults['PACMAN_SET_DEP'] = '-D' + SEP + '--asdeps'
defaults['IGNORE_GROUPS'] = 'base' + SEP + 'base-devel'

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
    # Remove empty lines
    lines = filter(lambda x: x, lines)
    # Remove comments
    lines = filter(lambda x: x[0] != '#', lines)
    lines = map(lambda x: x.split('#')[0], lines)
    # Split at equal sign
    lines = list(map(lambda x: x.split('='), lines))
    # Remove lines that have not exactly 2 values
    flags = filter(lambda x: len(x) == 1, lines)
    params = filter(lambda x: len(x) == 2, lines)
    # Handle flags
    flags = list(map(lambda x: x[0].strip(), flags))
    # Prepare to be transformed as a dict
    params = map(lambda x: (x[0].strip(), x[1].strip()), params)
    # Transform to dict
    params = OrderedDict(params)
    # Return configuration
    return flags, params


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
flags, user_conf = _read_conf(config_path)


def get(val, aslist=False):
    """Get a configuration value by its key.
    Return user defined value if existing, otherwise the defaults value. Raise
    an KeyError if the key is not existing in both.
    """
    result = None
    # If the user has defined the value return it
    if val in user_conf:
        result = user_conf[val]
    # If there is a default value return it
    elif val in defaults:
        result = defaults[val]
    # Raise an exception if not found
    if result is None:
        raise KeyError('Configuration key not existing.')
    # Return the result
    if aslist:
        return list(map(lambda x: x.strip(), result.split(SEP)))
    else:
        return result


def is_flag_set(name):
    """Return true if a configuration flag is set, false otherwise."""
    return name in flags
