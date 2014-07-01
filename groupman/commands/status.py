# -*- coding: utf-8 -*-
"""Give the status of the given group(s)."""

_name = 'status'
_help = 'give the status of the given group(s)'
order = 50


def add_to_subparsers(subparsers):
    parser = subparsers.add_parser(_name, help=_help)
    parser.set_defaults(cmd=run)


def run(args):
    # TODO write method
    # Get existing groups
    existing = list_groups()
    installed = db_list()
    print(">>> Installed")
    for group in installed:
            print(group)
    print(">>> Not Installed")
    for group in existing:
        if group not in installed:
            print(group)
