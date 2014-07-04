import groupman as gm
from distutils.core import setup

with open('README.rst') as f:
    long_description = f.read()

setup(name=gm.__appname__,
      version=gm.__version__,
      description=gm.__description__,
      long_description=long_description,
      author=gm.__author__,
      author_email=gm.__authormail__,
      url=gm.__projecturl__,
      packages=['groupman',
                'groupman.commands',
                'groupman.core',
                'groupman.extra',
                'groupman.utils'],
      scripts=['scripts/grpman'])
