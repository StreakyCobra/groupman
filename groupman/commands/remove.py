# -*- coding: utf-8 -*-
"""Remove the given group(s) of packages."""

from groupman.core.db import db_del
from groupman.core.groups import existing_groups, installed_groups
from groupman.core.prettyprint import pr, pr_info, pr_success, pr_warn

_name = 'remove'
_help = 'remove the given group(s) of packages'
order = 30


def add_to_subparsers(subparsers):
    parser = subparsers.add_parser(_name, help=_help)
    parser.add_argument('group',
                        type=str,
                        nargs='+',
                        help="the group(s) of packages to remove")
    parser.set_defaults(cmd=run)


def run(args):
    # Get existing packages
    existing = [x['name'] for x in existing_groups()]
    # Get installed packages
    installed = [x['name'] for x in installed_groups()]
    # Groups to uninstall
    to_uninstall = [g for g in args.group if g in existing and g in installed]
    # Groups not existing
    not_existing = [g for g in args.group if g not in existing]
    # Groups not installed
    not_installed = [g for g in args.group if g not in installed and g in existing]
    # Display not existing groups
    if not_existing:
        pr_warn('Groups not existing, skipped:')
        pr('\n'.join(not_existing))
    # Display not installed groups
    if not_installed:
        pr_info('Groups not installed:')
        pr('\n'.join(not_installed))
    # Remove groups
    if to_uninstall:
        # Add group in DB
        db_del(to_uninstall)
        pr_success('Groups successfully removed:')
        pr('\n'.join(to_uninstall))
