# -*- coding: utf-8 -*-
"""Pacman wrapper."""

from subprocess import call, check_output

from groupman.core.config import g
from groupman.core.prettyprint import pr_error
from groupman.core.utils import tbool


def pacman(args, force_sudo=None, output=True):
    """Run pacman with given arguments."""
    # Handle sudo
    cmd = ['sudo'] if tbool(g('PACMAN_SUDO')) else []
    # Handle force sudo
    if force_sudo is not None:
        cmd = ['sudo'] if force_sudo else []
    # Select caller regarding to the need of output or not
    caller = check_output if output else call
    try:
        # Call pacman
        output = caller(cmd + [g('PACMAN_CMD')] + args, universal_newlines=True)
        # Return the output
        return output
    except KeyboardInterrupt:
        pr_error("Cancelled")
