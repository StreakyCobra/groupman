# -*- coding: utf-8 -*-
"""Install the given group(s) of packages."""

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
    # Get groups
    groups = groups_info(args.group)
    # Add group in DB
    db_add([g['name'] for g in groups])
