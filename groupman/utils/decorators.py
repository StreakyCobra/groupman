# -*- coding: utf-8 -*-
"""Some decorators."""

import sys
from inspect import signature
from functools import wraps

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


@_debug_only
def trace(f):
    """Trace a function by printing all the call made."""
    @wraps(f)
    def wrapper(*args, **kw):
        kwstr = ', '.join('%r: %r' % (k, kw[k]) for k in sorted(kw))
        print("Calling %s() with args %s, {%s}" % (f.__name__, args, kwstr),
              file=sys.stderr)
        return f(*args, **kw)

    # Override signature
    wrapper.__signature__ = signature(f)

    return wrapper


def cache(f):
    """Cache the result of a function call regarding to its arguments."""
    @wraps(f)
    def wrapper(*args, **kw):
        # Ensure keywords arguments are hashable if existing
        if kw:
            key = args, frozenset(kw.items())
        else:
            key = args

        # Get the cache and set it if not already existing
        if '_cache' not in f.__dict__:
            f._cache = dict()
        cache = f._cache

        # If already computed, return cached result
        if key in cache:
            return cache[key]
        # Otherwise compute and cache results
        else:
            cache[key] = result = f(*args, **kw)
            return result

    # Override signature
    wrapper.__signature__ = signature(f)

    return wrapper


def once(f):
    """Ensure that a function is called only once."""
    @wraps(f)
    def wrapper(*args, **kw):
        if '_OK' not in f.__dict__:
            f._OK = True
            return f(*args, **kw)

    # Override signature
    wrapper.__signature__ = signature(f)

    return wrapper
