#!/usr/bin/env python

from distutils.core import setup

from bdd import __version__

#with open('README.rst', 'r'):
#    pass

setup(
    name='bdd',
    version=__version__,
    author='Windel Bouwman',
    py_modules=['bdd'],
    url='https://github.com/windel/bdd',
)
