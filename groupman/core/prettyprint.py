# -*- coding: utf-8 -*-
"""Pretty printing."""

import sys
from termcolor import colored

PROMPT = ':: '
PROMPT_COLOR = 'magenta'


def _print(msg, *args, **kwargs):
    _printn(msg + '\n', *args, **kwargs)


def _printn(msg, *args, **kwargs):
    sys.stdout.write(colored(msg, *args, **kwargs))


def _prompt():
    _printn(PROMPT, PROMPT_COLOR, attrs=['bold'])


def pr(msg):
    lines = msg.split('\n')
    for line in lines:
        _prompt()
        _print(line)


def pr_info(msg):
    _prompt()
    _print(msg, 'blue', attrs=['bold'])


def pr_success(msg):
    _prompt()
    _print(msg, 'green', attrs=['bold'])


def pr_warn(msg):
    _prompt()
    _print(msg, 'yellow', attrs=['bold'])


def pr_error(msg):
    _prompt()
    _print(msg, 'red', attrs=['bold'])


def pr_sep():
    _prompt()
    _print('- ' * 40, 'blue', attrs=['bold'])
