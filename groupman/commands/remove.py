# -*- coding: utf-8 -*-
"""Remove the given group(s) of packages."""

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
    # Get groups
    groups = groups_info(args.group, verify=False)
    # Add group in DB
    db_remove([g['name'] for g in groups])
