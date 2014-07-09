# -*- coding: utf-8 -*-
"""Helper to work with packages."""

from groupman.core.config import get
from groupman.core.pacman import pacman
from groupman.extra.groups import installed_groups


def _remove_unmanaged(packages):
    """Remove unmanaged ."""
    # Get unmanaged packages
    unmanaged = pacman(['-Qgq'] + get('IGNORE_GROUPS', aslist=True),
                       False).strip().split('\n')
    # Remove unmanaged packages
    filtered = [x for x in packages if x not in unmanaged]
    # Return the filtered list of packages
    return sorted(list(set(filtered)))


def all_installed_packages():
    """List all installed packages."""
    # Get all installed packages
    all_packages = pacman(['-Qq'], False).strip().split('\n')
    # Return all installed packages without unmanaged ones
    return _remove_unmanaged(all_packages)


def explict_installed_packages():
    """List explicitly installed packages without unmanaged ones."""
    # Get all explicitly installed packages
    explicit_packages = pacman(['-Qeq'], False).strip().split('\n')
    # Return all explicitly installed packages without unmanaged ones
    return _remove_unmanaged(explicit_packages)


def desired_packages():
    """List desired packages regarding to installed groups."""
    # Get all installed groups
    groups = installed_groups()
    # Get desired packages from groups
    desired = [p for group in groups for p in group['all_packages']]
    # Get unwanted packages from groups
    unwanted = [p for group in groups for p in group['all_removed']]
    # Remove unwanted packages
    desired = [p for p in desired if p not in unwanted]
    # Return desired packages without unmanaged ones
    return _remove_unmanaged(desired)
