#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Gather your Arch Linux packages in groups to simplify their management.
"""

import argparse
import os
import sys

from subprocess import call, check_output

__description__ = 'Gather your Arch Linux packages in groups to simplify their management.'


def print_err(msg):
    print(msg, file=sys.stderr)


def list_groups():
    # TODO Real method
    return ['aa', 'bb', 'cc', 'dmenu', 'acpi', 'scilab']


def group_info(group):
    # TODO Real method
    return {'name': group, 'path': group, 'packages': [group]}


def get_groups(groups):
    # Get existing groups
    existing = list_groups()

    # Prepare resulting list
    result = list()

    # Keep group only if existing
    for group in groups:
        if group in existing:
            result.append(group_info(group))
        else:
            print_err('Group "%s" is not existing: ignoring' % group)
    return result


def pacman(args, sudo=False):
    """Run pacman with given arguments."""
    cmd = ['sudo'] if sudo else []
    return check_output(cmd + ['pacman'] + args, universal_newlines=True)


def installed_packages():
    # Get all explicitly installed packages
    all_packages = pacman(['-Qeq']).strip().split('\n')
    # Get installed packages in group
    base_packages = pacman(['-Qgq', 'base', 'base-devel']).strip().split('\n')
    # Return all explicitly install package not in base
    return [x for x in all_packages if x not in base_packages]


def cmd_install(args):
    """Install group(s) of packages."""
    # Get groups
    groups = get_groups(args.group)
    # TODO Add groups in DB
    # Run an upgrade unless excplicitly specified
    if not args.noupgrade:
        cmd_upgrade(args)


def cmd_remove(args):
    """Remove group(s) of packages."""
    # Get groups
    groups = get_groups(args.group)
    # TODO Delete groups in DB
    # Run an upgrade unless excplicitly specified
    if not args.noupgrade:
        cmd_upgrade(args)


def cmd_upgrade(args):
    """Upgrade group(s) of packages."""
    # TODO Get real groups in DB
    groups_list = ['dmenu', 'acpi', 'test', 'scilab']
    # Get groups
    groups = get_groups(groups_list)
    # List of desired packages
    desired = [p for g in groups for p in g['packages']]
    # List of installed packages
    installed = installed_packages()
    # List of packages to install
    to_install = [x for x in desired if x not in installed]
    # List of packages to remove
    to_remove = [x for x in installed if x not in desired]
    print('\n'.join(to_install))
    print('*=' * 100)
    print('\n'.join(to_remove))


def cmd_edit(args):
    """Edit group(s) of packages."""
    # Get groups
    groups = get_groups(args.group)
    # Get files paths
    files = [x['path'] for x in groups]
    # Get prefered editor, 'vim' if not defined
    EDITOR = os.environ.get('EDITOR', 'vim')
    # If there is file to edit
    if files:
    # Call the editor to edit group files
        call([EDITOR] + files)
        # Run an upgrade unless excplicitly specified
        if not args.noupgrade:
            cmd_upgrade(args)


def main():
    # Global parser
    parser = argparse.ArgumentParser(description=__description__)

    # Subcommand parser
    subparsers = parser.add_subparsers()

    # Install command
    parser_install = subparsers.add_parser('install',
                                           help="install group(s) of packages")
    parser_install.add_argument('group',
                                type=str,
                                nargs='+',
                                help="group(s) of packages to install")
    parser_install.set_defaults(cmd=cmd_install)

    # Remove command
    parser_remove = subparsers.add_parser('remove',
                                          help="remove group(s) of packages")
    parser_remove.add_argument('group',
                               type=str,
                               nargs='+',
                               help="group(s) of packages to install")
    parser_remove.set_defaults(cmd=cmd_remove)

    # Upgrade groups
    parser_upgrade = subparsers.add_parser('upgrade',
                                           help="upgrade group(s) of packages")
    parser_upgrade.set_defaults(cmd=cmd_upgrade)

    # Edit command
    parser_edit = subparsers.add_parser('edit',
                                        help="edit group(s) of packages")
    parser_edit.add_argument('group',
                             type=str,
                             nargs='+',
                             help="group(s) of packages to install")
    parser_edit.add_argument('-n',
                             action="store_true",
                             dest="noupgrade",
                             help="don't do an upgrade after edition")
    parser_edit.set_defaults(cmd=cmd_edit)

    # Argrument: Update packages list
    parser.add_argument('-y',
                        action="store_true",
                        help="update package list with pacman first")

    # Complete: Used for command line completion
    parser.add_argument('--completion',
                        action="store_true",
                        help=argparse.SUPPRESS)

    # Parse arguments
    args = parser.parse_args()

    # Execute function associated to subcommand if existing else print help
    if 'cmd' in args:
        args.cmd(args)
    else:
        parser.print_help()

# When used as script
if __name__ == "__main__":
    main()
