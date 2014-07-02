# -*- coding: utf-8 -*-
"""Give the status of the packages."""

from groupman.core.db import db_list
from groupman.core.groups import group_info, installed_packages, deps_packages
from groupman.core.prettyprint import pr_list, pr_info

_name = 'packages'
_help = 'give the status of the packages'
order = 60


def add_to_subparsers(subparsers):
    parser = subparsers.add_parser(_name, help=_help)
    parser.set_defaults(cmd=run)


def run(args):
    # Get installed groups from DB
    groups = map(group_info, db_list())
    # List of needed packages
    desired = [d for group in groups for d in deps_packages(group['name'])]
    # List of installed packages
    installed = installed_packages()
    # List of packages to install
    to_install = list(set([x for x in desired if x not in installed]))
    # List of packages to remove
    to_remove = list(set([x for x in installed if x not in desired]))
    # Display packages
    if to_install:
        pr_info("Missing packages:", boxed=True)
        pr_list('\n'.join(to_install))
    if to_remove:
        pr_info("Supplementary packages:", boxed=True)
        pr_list('\n'.join(to_remove))
