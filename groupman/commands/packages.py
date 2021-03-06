# -*- coding: utf-8 -*-
"""Give the status of the packages."""

import sys

from groupman.extra.packages import explicit_installed_packages, desired_packages
from groupman.utils.display import pr_list, pr_info

_name = 'packages'
_help = 'give the status of the packages'
order = 60


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
    to_install = sorted([x for x in desired if x not in installed])
    # List of packages to remove
    to_remove = sorted([x for x in installed if x not in desired])
    # Remember if everything is up to date
    uptodate = True
    # Display packages
    if to_install:
        pr_info("Missing packages:", boxed=True)
        pr_list('\n'.join(to_install))
        uptodate = False
    if to_remove:
        pr_info("Extra packages:", boxed=True)
        pr_list('\n'.join(to_remove))
        uptodate = False
    if not uptodate:
        sys.exit(1)


def completion(args):
    sys.exit()
