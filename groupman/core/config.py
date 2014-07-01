# -*- coding: utf-8 -*-

__home__ = os.environ.get('HOME', '~')
__config__ = os.path.join(__home__, '.config/groupman')
__db__ = os.path.join(__config__, 'installed')
__groups__ = os.path.join(__config__, 'groups')

# Ensure configuration folder is existing
if not os.path.isdir(__config__):
    os.makedirs(__config__)
# Ensure groups folder is existing
if not os.path.isdir(__groups__):
    os.makedirs(__groups__)
# Ensure database is existing
if not os.path.isfile(__db__):
    with open(__db__, 'w') as f:
        f.write('')

