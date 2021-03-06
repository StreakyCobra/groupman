# -*- coding: utf-8 -*-
"""Remove the given group(s) of packages."""

import sys

from groupman.core.db import db_del
from groupman.extra.groups import existing_groups, installed_groups
from groupman.utils.display import pr_list, pr_info, pr_success, pr_warn

_name = 'remove'
_help = 'remove the given group(s) of packages'
order = 30


def add_to_subparsers(subparsers):
    parser = subparsers.add_parser(_name, help=_help)
    parser.add_argument('group',
                        type=str,
                        nargs='*',
                        help="the group(s) of packages to remove")
    parser.set_defaults(cmd=run)


def run(args):
    # If the completion is wanted
    if args.completion:
        completion(args)
    # Get existing groups
    existing = [x['name'] for x in existing_groups()]
    # Get installed groups
    installed = [x['name'] for x in installed_groups()]
    # Groups to uninstall
    to_uninstall = [g for g in args.group if g in existing and g in installed]
    # Groups not existing
    not_existing = [g for g in args.group if g not in existing]
    # Groups not installed
    not_installed = [g for g in args.group if g not in installed and g in existing]
    # Display not existing groups
    if not_existing:
        pr_warn('Groups not existing, skipped:', boxed=True)
        pr_list('\n'.join(not_existing))
    # Display not installed groups
    if not_installed:
        pr_info('Groups not installed:', boxed=True)
        pr_list('\n'.join(not_installed))
    # Remove groups
    if to_uninstall:
        # Add group in DB
        db_del(to_uninstall)
        pr_success('Groups successfully removed:', boxed=True)
        pr_list('\n'.join(to_uninstall))


def completion(args):
    # Get installed groups
    installed = [x['name'] for x in installed_groups()]
    # Propositions to print
    to_print = [group for group in installed if group not in args.group]
    # Print propositions
    if to_print:
        print('\n'.join(to_print))
    sys.exit()
