# -*- coding: utf-8 -*-
"""Helper to work with packages."""

from groupman.core.config import get
from groupman.core.pacman import pacman
from groupman.extra.groups import installed_groups
from groupman.utils.decorators import cache


@cache
def _unmanaged():
    # Get unmanaged packages
    unmanaged = pacman(["-Qg"], False).strip().split("\n")
    return unmanaged


def _remove_unmanaged(packages):
    """Remove unmanaged ."""
    # Get unmanaged packages
    unmanaged = _unmanaged()
    # Remove unmanaged packages
    filtered = [x for x in packages if x not in unmanaged]
    # Return the filtered list of packages
    return sorted(list(set(filtered)))


@cache
def all_installed_packages():
    """List all installed packages."""
    # Get all installed packages
    all_packages = pacman(['-Qq'], False).strip().split('\n')
    # Return all installed packages without unmanaged ones
    return _remove_unmanaged(all_packages)


@cache
def explicit_installed_packages():
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
