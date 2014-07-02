# -*- coding: utf-8 -*-
"""Give the status of the group(s)."""

from groupman.core.groups import existing_groups, installed_groups
from groupman.core.prettyprint import pr_list, pr_info

_name = 'status'
_help = 'give the status of the group(s)'
order = 50


def add_to_subparsers(subparsers):
    parser = subparsers.add_parser(_name, help=_help)
    parser.set_defaults(cmd=run)


def run(args):
    # Get existing groups
    existing = list(map(lambda x: x['name'], existing_groups()))
    # Get installed groups
    installed = list(map(lambda x: x['name'], installed_groups()))
    # Not installed groups
    not_installed = [group for group in existing if group not in installed]
    # Dependencies
    depends = [d for g in installed_groups() for d in g['depends'] if d not in installed]
    # Display installed packages
    if installed:
        pr_info("Installed (explicit):", boxed=True)
        pr_list('\n'.join(installed))
    # Display installed packages
    if depends:
        pr_info("Installed (dependency):", boxed=True)
        pr_list('\n'.join(depends))
    # Display not installed packages
    if not_installed:
        pr_info("Not installed", boxed=True)
        pr_list('\n'.join(not_installed))
