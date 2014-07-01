# -*- coding: utf-8 -*-

import os

import groupman.core.config as c

#def installed_packages():
#    """List explicitly installed packages that are not in base or base-devel."""
#    # Get all explicitly installed packages
#    all_packages = pacman(['-Qeq']).strip().split('\n')
#    # Get installed packages in base base-devel groupS
#    base_packages = pacman(['-Qgq', 'base', 'base-devel']).strip().split('\n')
#    # Return all explicitly install package not in base or base-devel
#    return [x for x in all_packages if x not in base_packages]
#
#
#def list_groups():
#    """List all available groups in the configuration folder."""
#    lst = os.listdir(__groups__)
#    files = filter(lambda x: os.path.isfile(os.path.join(__groups__, x)), lst)
#    return list(files)
#
#
def group_info(group):
    """Return informations about a given group."""
    path = os.path.join(c.groups_path, group)
    packages = []
    if os.path.isfile(path):
        with open(path, 'r') as f:
           packages = f.read().strip().split('\n')
    # TODO filter lines beginning with '#'
    return {'name': group, 'path': path, 'packages': packages}


def groups_info(groups, verify=True):
    """Return groups informations."""
    # Get existing groups
#    existing = list_groups()

    # Prepare resulting list
    result = list()

    # Keep group only if existing
    if groups:
        for group in groups:
#            if not verify or group in existing:
                result.append(group_info(group))
#            else:
#                print('Group "%s" is not existing: ignoring' % group)
#    else:
#        for group in existing:
#            result.append(group_info(group))
    return result
