# -*- coding: utf-8 -*-
"""Helper to manange groups and packages."""

import os
from collections import OrderedDict

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


def group_info(name):
    """Return informations about a given group name."""
    # Path to the group file
    path = os.path.join(c.groups_path, name)
    # Prepare the list of packages and depends
    packages = []
    depends = []
    # Read the file if existing
    if os.path.isfile(path):
        with open(path, 'r') as f:
            lines = f.readlines()
        # Strip lines
        lines = map(lambda x: x.strip(), lines)
        # Remove empty lines
        lines = filter(lambda x: x, lines)
        # Remove comments
        lines = filter(lambda x: x[0] != '#', lines)
        lines = list(map(lambda x: x.split('#')[0].strip(), lines))
        # Separate packages and groups
        packages = [x for x in lines if x[0] != '@']
        depends = [x[1:] for x in lines if x[0] == '@']
    return OrderedDict({'name': name,
                        'path': path,
                        'packages': packages,
                        'depends': depends})


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


def deps_groups(groupname):
    group = group_info(groupname)
    groups = group['depends']
    for dep in group['depends']:
        groups.extend(deps_groups(dep))
    return groups


def deps_packages(groupname):
    group = group_info(groupname)
    packages = group['packages']
    for dep in group['depends']:
        packages.extend(deps_packages(dep))
    return packages
