# -*- coding: utf-8 -*-
"""Update the system."""

import sys

from groupman.core.config import get
from groupman.core.pacman import pacman
from groupman.extra.packages import desired_packages, explicit_installed_packages
from groupman.utils.display import pr_list, pr_info

_name = 'update'
_help = 'update the system'
order = 40


def add_to_subparsers(subparsers):
    parser = subparsers.add_parser(_name, help=_help)
    parser.set_defaults(cmd=run)


def run(args):
    # If the completion is wanted
    if args.completion:
        completion(args)
    # List of needed packages
    desired = desired_packages()
    # List of installed packages
    installed = explicit_installed_packages()
    # List of packages to install
    to_install = list(set([x for x in desired if x not in installed]))
    # List of packages to remove
    to_remove = list(set([x for x in installed if x not in desired]))
    # Display packages
    if to_install:
        pr_info("Package(s) to install:", boxed=True)
        pr_list('\n'.join(sorted(to_install)))
    if to_remove:
        pr_info("Package(s) to remove:", boxed=True)
        pr_list('\n'.join(sorted(to_remove)))
    # Install missing packages
    if to_install:
        pr_info("Installing...")
        pacman(get('PACMAN_INSTALL', aslist=True) + ['--'] + to_install, output=False)
    # Remove unneeded packages
    if to_remove:
        pr_info("Removing...")
        pacman(get('PACMAN_REMOVE', aslist=True) + ['--'] + to_remove, output=False)


def completion(args):
    sys.exit()
