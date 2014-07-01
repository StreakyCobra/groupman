# -*- coding: utf-8 -*-
"""Update the system."""

_name = 'update'
_help = 'update the system'
order = 40


def add_to_subparsers(subparsers):
    parser = subparsers.add_parser(_name, help=_help)
    parser.set_defaults(cmd=run)


def run(args):
    # Get groups in DB
    groups_list = db_list()
    # Get groups
    groups = groups_info(groups_list, verify=False)
    # List of desired packages
    desired = [p for g in groups for p in g['packages']]
    # List of installed packages
    installed = installed_packages()
    # List of packages to install
    to_install = [x for x in desired if x not in installed]
    # List of packages to remove
    to_remove = [x for x in installed if x not in desired]
    print('Will install: %s' % to_install)
    print('Will remove: %s' % to_remove)
    # Install missing packages
    if to_install:
        pacman(['-S'] +  to_install, sudo=True, output=False)
    if to_remove:
        pacman(['-Rs'] +  to_remove, sudo=True, output=False)
