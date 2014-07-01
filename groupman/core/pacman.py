# -*- coding: utf-8 -*-

from subprocess import call, check_output


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
