# -*- coding: utf-8 -*-
"""Update the system."""

from groupman.core.config import g
from groupman.core.db import db_list
from groupman.core.groups import group_info, installed_packages
from groupman.core.pacman import pacman
from groupman.core.prettyprint import pr, pr_info

_name = 'update'
_help = 'update the system'
order = 40


def add_to_subparsers(subparsers):
    parser = subparsers.add_parser(_name, help=_help)
    parser.set_defaults(cmd=run)


def run(args):
    # Get installed groups from DB
    groups = map(group_info, db_list())
    # List of needed packages
    desired = [p for group in groups for p in group['packages']]
    # List of installed packages
    installed = installed_packages()
    # List of packages to install
    to_install = list(set([x for x in desired if x not in installed]))
    # List of packages to remove
    to_remove = list(set([x for x in installed if x not in desired]))
    # Display packages
    if to_install:
        pr_info("Package(s) to install:")
        pr('\n'.join(to_install))
    if to_remove:
        pr_info("Package(s) to remove:")
        pr('\n'.join(to_remove))
    # Install missing packages
    if to_install:
        pr_info("Installing...")
        pacman([g('PACMAN_INSTALL')] + to_install, output=False)
    # Remove unneeded packages
    if to_remove:
        pr_info("Removing...")
        pacman([g('PACMAN_REMOVE')] + to_remove, output=False)
