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
__home__ = os.environ.get('HOME', '~')
__config__ = os.path.join(__home__, '.config/groupman')
__db__ = os.path.join(__config__, 'installed')
__groups__ = os.path.join(__config__, 'groups')

# Ensure configuration folder is existing
if not os.path.isdir(__config__):
    os.makedirs(__config__)
# Ensure groups folder is existing
if not os.path.isdir(__groups__):
    os.makedirs(__groups__)
# Ensure database is existing
if not os.path.isfile(__db__):
    with open(__db__, 'w') as f:
        f.write('')


def print_err(msg):
    """Print an error message."""
    print(msg, file=sys.stderr)


def list_groups():
    """List all available groups in the configuration folder."""
    lst = os.listdir(__groups__)
    files = filter(lambda x: os.path.isfile(os.path.join(__groups__, x)), lst)
    return list(files)


def group_info(group):
    """Return informations about a given group."""
    name = group
    path = os.path.join(__groups__, group)
    packages = []
    if os.path.isfile(path):
        with open(path, 'r') as f:
            packages = f.read().strip().split('\n')
    # TODO filter lines beginning with '#'
    return {'name': group, 'path': path, 'packages': packages}


def groups_info(groups, verify=True):
    """Return groups informations."""
    # Get existing groups
    existing = list_groups()

    # Prepare resulting list
    result = list()

    # Keep group only if existing
    if groups:
        for group in groups:
            if not verify or group in existing:
                result.append(group_info(group))
            else:
                print_err('Group "%s" is not existing: ignoring' % group)
    else:
        for group in existing:
            result.append(group_info(group))
    return result


def pacman(args, sudo=False, output=True):
    """Run pacman with given arguments."""
    # Handle sudo
    cmd = ['sudo'] if sudo else []
    # Select caller regarding to needs
    caller = check_output if output else call
    # For later use
    pacman_cmd = 'pacman'
    # Call pacman
    return caller(cmd + [pacman_cmd] + args, universal_newlines=True)


def installed_packages():
    """List explicitly installed packages that are not in base or base-devel."""
    # Get all explicitly installed packages
    all_packages = pacman(['-Qeq']).strip().split('\n')
    # Get installed packages in base base-devel groupS
    base_packages = pacman(['-Qgq', 'base', 'base-devel']).strip().split('\n')
    # Return all explicitly install package not in base or base-devel
    return [x for x in all_packages if x not in base_packages]


def db_list():
    """List all packages into the database."""
    # Read packages
    with open(__db__, 'r') as f:
        lst = f.read().strip().split('\n')
    # Return the list
    return lst


def db_add(groups):
    """Add some groups to the database."""
    # Read packages
    with open(__db__, 'r') as f:
        lst = f.read().strip().split('\n')
    # Add and sort packages list
    lst += groups
    lst = list(sorted(list(set(lst))))
    # Write modified packages list
    with open(__db__, 'w') as f:
        f.write('\n'.join(lst) + '\n')


def db_remove(groups):
    """Remove some groups from the database."""
    # Read packages
    with open(__db__, 'r') as f:
        lst = f.read().strip().split('\n')
    # Remove and sort packages list
    lst = [l for l in lst if not l in groups]
    lst = list(sorted(list(set(lst))))
    # Write modified packages list
    with open(__db__, 'w') as f:
        f.write('\n'.join(lst) + '\n')


def cmd_init(args):
    """Initialize a 'base' group with all repositories."""
    if os.listdir(__groups__):
        print_err("Already existing groups")
        return
    # Get packages
    packages = installed_packages()
    # Create base group with all packages
    with open(os.path.join(__groups__, 'base'), 'w') as f:
        f.write('\n'.join(packages))


def cmd_status(args):
    """Get the status of packages and groups."""
    # TODO write method
    for group in db_list():
        print(group)


def cmd_install(args):
    """Install group(s) of packages."""
    # Get groups
    groups = groups_info(args.group)
    # Add group in DB
    db_add([g['name'] for g in groups])


def cmd_remove(args):
    """Remove group(s) of packages."""
    # Get groups
    groups = groups_info(args.group, verify=False)
    # Add group in DB
    db_remove([g['name'] for g in groups])


def cmd_upgrade(args):
    """Upgrade group(s) of packages."""
    # Get groups in DB
    groups_list = db_list()
    # Get groups
    groups = groups_info(groups_list, verify=False)
    # List of desired packages
    desired = [p for g in groups for p in g['packages']]
    # List of installed packages
    installed = installed_packages()
    # List of packages to install
    to_install = [x for x in desired if x not in installed]
    # List of packages to remove
    to_remove = [x for x in installed if x not in desired]
    print('Will install: %s' % to_install)
    print('Will remove: %s' % to_remove)
    # Install missing packages
    if to_install:
        pacman(['-S'] +  to_install, sudo=True, output=False)
    if to_remove:
        pacman(['-Rs'] +  to_remove, sudo=True, output=False)


def cmd_edit(args):
    """Run the default editor to edit specific group(s) of packages."""
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


def main():
    """Entry point of the program."""
    # Global parser
    parser = argparse.ArgumentParser(description=__description__)

    # Subcommand parser
    subparsers = parser.add_subparsers()

    # Init command
    parser_init = subparsers.add_parser('init',
                                        help="init groupman")
    parser_init.set_defaults(cmd=cmd_init)

    # Status command
    parser_status = subparsers.add_parser('status',
                                          help="Packages and groups status")
    parser_status.set_defaults(cmd=cmd_status)

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
                             nargs='*',
                             help="group(s) of packages to install")
    parser_edit.set_defaults(cmd=cmd_edit)

    # Update packages first
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
