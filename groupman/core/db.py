# -*- coding: utf-8 -*-
"""Manage the database."""

import groupman.core.config as conf


def _db_read():
    """Parse the database file and return the list of groups."""
    # Read groups from db
    with open(conf.db_path, 'r') as f:
        lst = f.read().strip().split('\n')
    # Remove empty lines
    lst = filter(lambda x: x, lst)
    # Return list of groups
    return list(lst)


def _db_write(lst):
    """Write the list of groups in the database file."""
    # Remove duplicates and sort the groups
    lst = list(sorted(list(set(lst))))
    # Write groups to db
    with open(conf.db_path, 'w') as f:
        f.write('\n'.join(lst) + '\n')


def db_list():
    """List all packages in the database."""
    return _db_read()


def db_add(groups):
    """Add the given group(s) to the database."""
    # Get list of groups
    lst = _db_read()
    # Add and sort packages list
    lst += groups
    # Write new list to the database
    _db_write(lst)


def db_del(groups):
    """Delete the given group(s) from the database."""
    # Get list of groups
    lst = _db_read()
    # Delete groups from list
    lst = [g for g in lst if g not in groups]
    # Write new list to the database
    _db_write(lst)
