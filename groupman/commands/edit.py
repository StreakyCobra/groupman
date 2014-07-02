# -*- coding: utf-8 -*-
"""Edit the given group(s) of packages."""

from subprocess import call

from groupman.core.config import g
from groupman.core.groups import group_info

_name = 'edit'
_help = 'edit the given group(s) of packages'
order = 60


def add_to_subparsers(subparsers):
    parser = subparsers.add_parser(_name, help=_help)
    parser.add_argument('group',
                        type=str,
                        nargs='*',
                        help="the group(s) of packages to edit")
    parser.set_defaults(cmd=run)


def run(args):
    # Get groups
    groups = map(group_info, args.group)
    # Get files paths
    files = [x['path'] for x in groups]
    # If there is file to edit
    if files:
        # Call the editor to edit group files
        call([g('EDITOR')] + files)
