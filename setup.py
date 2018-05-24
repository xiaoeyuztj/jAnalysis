import os

from setuptools import setup, find_packages
#from codecs import open as codecs_open

here = os.path.abspath( os.path.dirname(__file__))

# setup jROOT
about = {}
with open( os.path.join( here, 'jROOT', '__version__.py'), 'r') as f:
    exec(f.read(), about)
setup(
        name = about['__title__'],
        version = about['__version__'],
        description = about['__description__'],
        url = about['__url__'],
        author = about['__author__'],
        author_email = about['__author_email__']
        )

# setup VBSZZ
about = {}
with open( os.path.join( here, 'VBSZZ', '__version__.py'), 'r') as f:
    exec(f.read(), about)
setup(
        name = about['__title__'],
        version = about['__version__'],
        description = about['__description__'],
        url = about['__url__'],
        author = about['__author__'],
        author_email = about['__author_email__']
        )
