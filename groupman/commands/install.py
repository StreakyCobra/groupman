# -*- coding: utf-8 -*-
"""Install the given group(s) of packages."""

from groupman.core.db import db_add
from groupman.core.groups import existing_groups, installed_groups
from groupman.core.prettyprint import pr, pr_info, pr_success, pr_warn

_name = 'install'
_help = 'install the given group(s) of packages'
order = 20


def add_to_subparsers(subparsers):
    parser = subparsers.add_parser(_name, help=_help)
    parser.add_argument('group',
                        type=str,
                        nargs='+',
                        help="the group(s) of packages to install")
    parser.set_defaults(cmd=run)


def run(args):
    # Get existing packages
    existing = [x['name'] for x in existing_groups()]
    # Get installed packages
    installed = [x['name'] for x in installed_groups()]
    # Groups to install
    to_install = [g for g in args.group if g in existing and g not in installed]
    # Groups not existing
    not_existing = [g for g in args.group if g not in existing]
    # Groups already installed
    already_installed = [g for g in args.group if g in installed]
    # Display not existing groups
    if not_existing:
        pr_warn('Groups not existing, skipped:')
        pr('\n'.join(not_existing))
    # Display not found groups
    if already_installed:
        pr_info('Groups already installed:')
        pr('\n'.join(already_installed))
    # Install missing groups
    if to_install:
        # Add group in DB
        db_add(to_install)
        pr_success('Groups successfully installed:')
        pr('\n'.join(to_install))
