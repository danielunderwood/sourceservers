"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages

import sourceservers

setup(
    # Project info
    name='sourceservers',
    version=sourceservers.__version__,
    description='Web API to perform source server queries',
    url='https://github.com/danielunderwood/sourceservers',

    # Author details
    author='Daniel Underwood',
    author_email='daniel@sourceservers.org',

    # Choose your license
    license='Apache 2.0',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=['flask', 'python-valve'],

    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    extras_require={
    },
)
