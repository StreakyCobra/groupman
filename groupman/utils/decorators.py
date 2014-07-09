# -*- coding: utf-8 -*-
"""Some decorators."""

import sys
from decorator import decorator

from groupman.core.config import is_flag_set


def _identity(f, *args, **kw):
    """Identity function for @decorator functions."""
    # Do nothing, just apply the function
    return f(*args, **kw)


def _debug_only(f):
    """Decorator to specify decorator that must be used only in debug mode."""
    # If debug mode is set, return the written decorator
    if is_flag_set('DEBUG'):
        return f
    # Otherwise return the identity function that do nothing special,
    # i.e. disable the decorator
    else:
        return _identity


@decorator
@_debug_only
def trace(f, *args, **kw):
    """Trace a function by printing all the call made."""
    kwstr = ', '.join('%r: %r' % (k, kw[k]) for k in sorted(kw))
    print("Calling %s() with args %s, {%s}" % (f.__name__, args, kwstr),
          file=sys.stderr)
    return f(*args, **kw)


@decorator
def cache(func, *args, **kw):
    """Cache the result of a function call regarding to its arguments."""
    # Ensure keywords arguments are hashable if existing
    if kw:
        key = args, frozenset(kw.iteritems())
    else:
        key = args

    # Get the cache and set it if not already existing
    if '_cache' not in func.__dict__:
        func._cache = dict()
    cache = func._cache

    # If already computed, return cached result
    if key in cache:
        return cache[key]
    # Otherwise compute and cache results
    else:
        cache[key] = result = func(*args, **kw)
        return result


@decorator
def once(func, *args, **kw):
    """Ensure that a function is called only once."""
    if '_OK' not in func.__dict__:
        func._OK = True
        return func(*args, **kw)
