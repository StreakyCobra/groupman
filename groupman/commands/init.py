# -*- coding: utf-8 -*-
"""Initialize the system with already installed packages."""

import os

_name = 'init'
_help = 'initialize the system with already installed packages.'
order = 10


def add_to_subparsers(subparsers):
    parser = subparsers.add_parser(_name, help=_help)
    parser.set_defaults(cmd=run)


def run(args):
    if os.listdir(__groups__):
        print_err("Already existing groups")
        return
    # Get packages
    packages = installed_packages()
    # Create base group with all packages
    with open(os.path.join(__groups__, 'base'), 'w') as f:
        f.write('\n'.join(packages))
