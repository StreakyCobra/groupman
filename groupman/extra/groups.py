# -*- coding: utf-8 -*-
"""Helper to work with groups."""

import os
from collections import OrderedDict

import groupman.core.config as conf
from groupman.core.db import db_list, db_del
from groupman.utils.decorators import cache, once

SYM_GROUP = '@'
SYM_REMOVE = '/'
SYM_COMMENT = '#'


def _parse(lines):
    """Parse a group file and return its dependencies and packages."""
    # Copy the list
    parsed = list(lines)
    # Strip lines
    parsed = map(lambda x: x.strip(), parsed)
    # Remove empty lines
    parsed = filter(lambda x: x, parsed)
    # Remove comments
    parsed = filter(lambda x: x[0] != SYM_COMMENT, parsed)
    parsed = map(lambda x: x.split(SYM_COMMENT)[0].strip(), parsed)
    # Remove empty lines
    parsed = list(filter(lambda x: x, parsed))
    # Extract packages
    packages = [x for x in parsed if x[0] != SYM_GROUP and x[0] != SYM_REMOVE]
    # Extract depends
    depends = [x[1:] for x in parsed if x[0] == SYM_GROUP]
    # Extract depends
    removed = [x[1:] for x in parsed if x[0] == SYM_REMOVE]
    # Return the result of parsing
    return (sorted(list(set(depends))),
            sorted(list(set(packages))),
            sorted(list(set(removed))))


@cache
def _parse_recursive(name):
    # Get non recursive information about the group
    group = group_info(name, recursive=False)
    # Get packages and depends
    depends = list(group['depends'])
    packages = list(group['packages'])
    removed = list(group['removed'])
    # Recursive generation of depends and packages
    for dep in group['depends']:
        rec_depends, rec_packages, rec_removed = _parse_recursive(dep)
        depends += rec_depends
        packages += rec_packages
        removed += rec_removed
    # Return results
    return (sorted(list(set(depends))),
            sorted(list(set(packages))),
            sorted(list(set(removed))))


@cache
def group_info(name, recursive=True):
    """Return informations about a given group name."""
    # Path to the group file
    path = os.path.join(conf.groups_path, name)
    # Prepare the list of packages and depends
    packages = []
    depends = []
    removed = []
    if recursive:
        all_packages = []
        all_depends = []
        all_removed = []
    # Read the file if existing
    if os.path.isfile(path):
        with open(path, 'r') as f:
            depends, packages, removed = _parse(f.readlines())
        if recursive:
            all_depends, all_packages, all_removed = _parse_recursive(name)
    # Prepare the result
    info = OrderedDict()
    info['name'] = name
    info['path'] = path
    info['depends'] = depends
    info['packages'] = packages
    info['removed'] = removed
    if recursive:
        info['all_depends'] = all_depends
        info['all_packages'] = all_packages
        info['all_removed'] = all_removed
    # Return the informations
    return info


@cache
def _existing_groups_names():
    """List all available groups names in the configuration folder."""
    # List the content of the groups folder
    lst = os.listdir(conf.groups_path)
    # Keep only files
    files = filter(lambda x: os.path.isfile(os.path.join(conf.groups_path, x)), lst)
    # Return the resulting list of groups names
    return sorted(list(set(files)))


@cache
def existing_groups():
    """List all available groups in the configuration folder."""
    # Get all existing groups
    lst = _existing_groups_names()
    # Read and return groups
    return list(map(group_info, lst))


def installed_groups():
    """List all installed groups."""
    # Get all groups in db
    lst = db_list()
    # Read and return groups
    return list(map(group_info, lst))


@once
def check_groups():
    """Verify that installed groups in db are still existing."""
    # Get installed groups
    installed = list(map(lambda x: x['name'], installed_groups()))
    # Get existing groups
    existing = list(map(lambda x: x['name'], existing_groups()))
    # List unexisting installed groups
    missing = [x for x in installed if x not in existing]
    # Check if any:
    if missing:
        # Remove them from db
        for x in missing:
            db_del(x)


# Check group when this module is loaded, but only if not in completion mode
check_groups()
