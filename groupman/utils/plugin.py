# -*- coding: utf-8 -*-
"""Utility function to make plugin system."""

import pkgutil
import importlib


def load_module(module_name):
    """Load and return a module dynamically from its name."""
    # Load the module dynamically
    mod = importlib.import_module(module_name)
    # Return the module
    return mod


def load_package_modules(package):
    """Load all modules in a given package, return their names and the module."""
    # The path to the package
    pkgpath = package.__path__
    # The package name
    pkgname = package.__package__
    # Get all modules names present in the package
    names = [name for __, name, __ in pkgutil.iter_modules(pkgpath)]
    # Load each modules
    modules = [load_module('%s.%s' % (pkgname, name)) for name in names]
    # Return a list of pair of names and modules
    return zip(names, modules)
