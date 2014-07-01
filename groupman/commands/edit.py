# -*- coding: utf-8 -*-
"""Edit the given group(s) of packages."""

import os

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
    groups = groups_info(args.group, verify=False)
    # Get files paths
    files = [x['path'] for x in groups]
    # Get prefered editor, 'vim' if not defined
    EDITOR = os.environ.get('EDITOR', 'vim')
    # If there is file to edit
    if files:
        # Call the editor to edit group files
        call([EDITOR] + files)
