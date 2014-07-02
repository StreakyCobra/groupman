# -*- coding: utf-8 -*-
"""Initialize the system with already installed packages."""

import os
import sys

import groupman.core.config as c
from groupman.core.db import db_add
from groupman.core.groups import installed_packages
from groupman.core.prettyprint import pr_success, pr_error

_name = 'init'
_help = 'initialize the system with already installed packages.'
order = 10


def add_to_subparsers(subparsers):
    parser = subparsers.add_parser(_name, help=_help)
    parser.set_defaults(cmd=run)


def run(args):
    # Verify if packages are not already existing
    if os.listdir(c.groups_path):
        pr_error("There is already existing groups, "
                 "will not initalize a second time")
        sys.exit(1)
    # Get installed packages
    packages = installed_packages()
    # Create a base group with installed packages
    with open(os.path.join(c.groups_path, 'base'), 'w') as f:
        f.write('\n'.join(packages))
    # Add base group to db
    db_add(['base'])
    # Print
    pr_success('Initialization complete. A `base` packages has been created.')