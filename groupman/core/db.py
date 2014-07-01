# -*- coding: utf-8 -*-


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


