# -*- coding: utf-8 -*-

import argparse

import groupman as gm
import groupman.commands
from groupman.core.utils import load_package_modules

# The package containing the commands
cmd_package = groupman.commands


def _plug_commands(subparsers):
    """Load and plug-in dynamically all modules present in the commands
    package."""
    # List modules
    modules = load_package_modules(cmd_package)
    # Load each module and add plug-it in to the subparsers
    for _, mod in sorted(modules, key=lambda x: x[1].order):
        mod.add_to_subparsers(subparsers)


def run():
    """Entry point of the application."""
    # Global parser
    parser = argparse.ArgumentParser(description=gm.__description__)

    # Subcommand parser
    subparsers = parser.add_subparsers()

    # Plug-in all modules present in the commands package.
    _plug_commands(subparsers)

    # Flag to show the version number
    parser.add_argument('-v',
                        action="store_true",
                        dest='version',
                        help="print the version number and exit")

    # Flag to update pacman first
    parser.add_argument('-y',
                        action="store_true",
                        help="update package list with pacman first")

    # Flag for command line completion
    parser.add_argument('--completion',
                        action="store_true",
                        help=argparse.SUPPRESS)

    # Parse arguments
    args = parser.parse_args()

    # If the version is wanted, print it
    if args.version:
        print(gm.__version__)
    # If existing, execute the function associated with the subcommand
    elif 'cmd' in args:
        args.cmd(args)
    # If the completion is wanted
    elif args.completion:
        for name, _ in load_package_modules(cmd_package):
            print(name)
    # Otherwise print the help message
    else:
        parser.print_help()


# When used as a script
if __name__ == "__main__":
    run()
