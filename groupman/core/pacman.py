# -*- coding: utf-8 -*-
"""Pacman wrapper."""

from subprocess import call, check_output

from groupman.core.config import get


def _parse_bool(val):
    """Helper function that transform text to bool.
    Return true is `val` is equal (in lowercase) with:
        - yes
        - true
        - t
        - 1
    """
    return val.lower() in ('yes', 'true', 't', '1')


def pacman(args, force_sudo=None, output=True):
    """Run pacman with given arguments."""
    # Handle sudo
    cmd = ['sudo'] if _parse_bool(get('PACMAN_SUDO')) else []
    # Handle force sudo
    if force_sudo is not None:
        cmd = ['sudo'] if force_sudo else []
    # Select caller regarding to the need of output or not
    caller = check_output if output else call
    # Call pacman
    output = caller(cmd + [get('PACMAN_CMD')] + args, universal_newlines=True)
    # Return the output
    return output
