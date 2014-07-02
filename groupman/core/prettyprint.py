# -*- coding: utf-8 -*-
"""Pretty printing."""

import sys
from termcolor import colored

PROMPT_COLOR = 'magenta'

PROMPT     = '»» '

LIST_START = '»┍ '
LIST       = ' │ '
LIST_END   = ' └ '


def _print(msg, *args, **kwargs):
    _printn(msg + '\n', *args, **kwargs)


def _printn(msg, *args, **kwargs):
    sys.stdout.write(colored(msg, *args, **kwargs))


def _prompt(sym=None, boxed=False):
    if sym is None:
        sym = PROMPT
        if boxed:
            sym = LIST_START
    _printn(sym, PROMPT_COLOR, attrs=['bold'])


def pr_list(msg):
    lines = msg.split('\n')
    for line in lines[:-1]:
        _prompt(sym=LIST)
        _print(line)
    _prompt(sym=LIST_END)
    _print(lines[-1])


def pr_info(msg, **kwargs):
    _prompt(**kwargs)
    _print(msg, 'blue', attrs=['bold'])


def pr_success(msg, **kwargs):
    _prompt(**kwargs)
    _print(msg, 'green', attrs=['bold'])


def pr_warn(msg, **kwargs):
    _prompt(**kwargs)
    _print(msg, 'yellow', attrs=['bold'])


def pr_error(msg, **kwargs):
    _prompt(**kwargs)
    _print(msg, 'red', attrs=['bold'])
