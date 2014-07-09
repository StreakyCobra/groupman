# -*- coding: utf-8 -*-
"""Helper to work with packages."""

from groupman.core.config import get
from groupman.core.pacman import pacman
from groupman.extra.groups import installed_groups


def remove_unmanaged(packages):
    # Get unmanaged packages
    unmanaged = pacman(['-Qgq'] + get('IGNORE_GROUPS', aslist=True),
                       False).strip().split('\n')
    # Remove unmanaged packages
    filtered = [x for x in packages if x not in unmanaged]
    return sorted(list(set(filtered)))


def all_installed_packages():
    """List explicitly installed packages that are not in base or base-devel."""
    # Get all explicitly installed packages
    explicit_packages = pacman(['-Qq'], False).strip().split('\n')
    # Return all explicitly install package without unmanaged ones
    return remove_unmanaged(explicit_packages)


def explict_installed_packages():
    """List explicitly installed packages that are not in base or base-devel."""
    # Get all explicitly installed packages
    explicit_packages = pacman(['-Qeq'], False).strip().split('\n')
    # Return all explicitly install package without unmanaged ones
    return remove_unmanaged(explicit_packages)


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
    # Remove unmanaged packages
    desired = remove_unmanaged(desired)
    # Return desired packages
    return desired
