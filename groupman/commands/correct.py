# -*- coding: utf-8 -*-
"""Update the system."""

import sys

from groupman.core.config import get
from groupman.core.pacman import pacman
from groupman.extra.packages import desired_packages, explicit_installed_packages, all_installed_packages
from groupman.utils.display import pr_list, pr_info

_name = 'correct'
_help = 'correct explicit/dependency flags in pacman database'
order = 80


def add_to_subparsers(subparsers):
    parser = subparsers.add_parser(_name, help=_help)
    parser.set_defaults(cmd=run)


def run(args):
    # If the completion is wanted
    if args.completion:
        completion(args)

    # List of desired packages
    desired = desired_packages()
    # List of all installed packages
    all_packages = all_installed_packages()
    # List of explicitly installed packages
    explicit = explicit_installed_packages()
    # List of all packages installed as dependency
    dependency = [x for x in all_packages if x not in explicit]

    # List of packages to install
    to_explicit = list(set([x for x in dependency if x in desired]))
    # List of packages to remove
    to_dependency = list(set([x for x in explicit if x not in desired]))

    # Display packages
    if to_explicit:
        pr_info("Package(s) to set as explicitly installed:", boxed=True)
        pr_list('\n'.join(sorted(to_explicit)))
    if to_dependency:
        pr_info("Package(s) to set as installed as dependency:", boxed=True)
        pr_list('\n'.join(sorted(to_dependency)))
    # Install missing packages
    if to_explicit:
        pr_info("Setting explicit...")
        pacman(get('PACMAN_SET_EXP', aslist=True) + ['--'] + to_explicit, output=False)
    # Remove unneeded packages
    if to_dependency:
        pr_info("Setting dependency...")
        pacman(get('PACMAN_SET_DEP', aslist=True) + ['--'] + to_dependency, output=False)


def completion(args):
    sys.exit()
