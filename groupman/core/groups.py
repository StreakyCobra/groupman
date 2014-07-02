# -*- coding: utf-8 -*-
"""Helper to manange groups and packages."""

import os

import groupman.core.config as c
from groupman.core.pacman import pacman
from groupman.core.db import db_list


def installed_packages():
    """List explicitly installed packages that are not in base or base-devel."""
    # Get all explicitly installed packages
    explicit_packages = pacman(['-Qeq'],
                               False).strip().split('\n')
    # Get installed packages in base base-devel groupS
    base_packages = pacman(['-Qgq', 'base', 'base-devel'],
                           False).strip().split('\n')
    # Return all explicitly install package not in base or base-devel
    return [x for x in explicit_packages if x not in base_packages]


def group_info(group):
    """Return informations about a given group."""
    # TODO complex parsing here
    # TODO filter lines beginning with '#'
    path = os.path.join(c.groups_path, group)
    packages = []
    if os.path.isfile(path):
        with open(path, 'r') as f:
            packages = f.read().strip().split('\n')
    return {'name': group, 'path': path, 'packages': packages}


def _existing_groups_names():
    """List all available groups names in the configuration folder."""
    # List the content of the groups folder
    lst = os.listdir(c.groups_path)
    # Keep only files
    files = filter(lambda x: os.path.isfile(os.path.join(c.groups_path, x)), lst)
    # Return the resulting list of groups names
    return list(files)


def existing_groups():
    """List all available groups in the configuration folder."""
    # List all groups in db
    lst = _existing_groups_names()
    # Read and return groups
    return list(map(group_info, lst))


def installed_groups():
    """List all installed groups."""
    # List all groups in db
    lst = db_list()
    # Read and return groups
    return list(map(group_info, lst))
