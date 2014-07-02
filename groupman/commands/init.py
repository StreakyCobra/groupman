# -*- coding: utf-8 -*-
"""Initialize the system with already installed packages."""

import os

import groupman.core.config as c
from groupman.core.config import g
from groupman.core.db import db_add, db_list
from groupman.core.groups import installed_packages

_name = 'init'
_help = 'initialize the system with already installed packages.'
order = 10


def add_to_subparsers(subparsers):
    parser = subparsers.add_parser(_name, help=_help)
    parser.set_defaults(cmd=run)


def run(args):
    # Verify if packages are not already existing
    if os.listdir(c.groups_path):
        print("There is already configured groups.")
        return
    print(db_list())
    # Get installed packages
    packages = installed_packages()
    # Create a base group with installed packages
    with open(os.path.join(c.groups_path, 'base'), 'w') as f:
        f.write('\n'.join(packages))
    # Add base group to db
    db_add(['base'])
