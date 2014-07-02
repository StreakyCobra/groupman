import groupman
from distutils.core import setup

with open('README.rst') as f:
    long_description = f.read()

setup(name=pws.__appname__,
      version=pws.__version__,
      description=pws.__description__,
      long_description=long_description,
      author=pws.__author__,
      author_email=pws.__authormail__,
      url=pws.__projecturl__,
      packages=['groupman',
                'groupman.commands',
                'groupman.core'],
      scripts=['grpman'])
