# -*- coding: utf-8 -*-
"""Helper to work with packages."""

from groupman.core.pacman import pacman
from groupman.extra.groups import installed_groups


def installed_packages():
    """List explicitly installed packages that are not in base or base-devel."""
    # Get all explicitly installed packages
    explicit_packages = pacman(['-Qeq'], False).strip().split('\n')
    # Get installed packages in base base-devel groupS
    base_packages = pacman(['-Qgq', 'base'], False).strip().split('\n')
    # Return all explicitly install package not in base or base-devel
    return [x for x in explicit_packages if x not in base_packages]


def desired_packages():
    """List desired packages regarding to installed groups."""
    # Get all installed groups
    groups = installed_groups()
    # Get desired packages from groups
    desired = [p for group in groups for p in group['all_packages']]
    # Return cleaned and sorted list of packags
    return sorted(list(set(desired)))
