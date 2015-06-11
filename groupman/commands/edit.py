# -*- coding: utf-8 -*-
"""Edit the given group(s) of packages."""

import sys
from subprocess import call

from groupman.core.config import get
from groupman.extra.groups import group_info, existing_groups
from groupman.utils.display import pr_list, pr_info, pr_warn

_name = 'edit'
_help = 'edit the given group(s) of packages'
order = 70


def add_to_subparsers(subparsers):
    parser = subparsers.add_parser(_name, help=_help)
    parser.add_argument('group',
                        type=str,
                        nargs='*',
                        help="the group(s) of packages to edit")
    parser.set_defaults(cmd=run)


def run(args):
    # If the completion is wanted
    if args.completion:
        completion(args)
    # Get groups
    if args.group:
        groups = list(map(group_info, args.group))
    else:
        groups = existing_groups()
    # Get files paths
    files = [x['path'] for x in groups]
    # If there is file to edit
    if files:
        pr_info('The following groups will be edited:', boxed=True)
        pr_list('\n'.join([x['name'] for x in groups]))
        # Call the editor
        call([get('EDITOR'), '--'] + files)
    else:
        pr_warn('No files to edit')


def completion(args):
    # Get existing groups
    existing = [x['name'] for x in existing_groups()]
    # Propositions to print
    to_print = [group for group in existing if group not in args.group]
    # Print propositions
    if to_print:
        print('\n'.join(to_print))
    sys.exit()
