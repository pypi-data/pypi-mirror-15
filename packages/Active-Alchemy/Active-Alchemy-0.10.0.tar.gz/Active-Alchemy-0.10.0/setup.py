# -*- coding: utf-8 -*-
"""
==================
Active-Alchemy
==================

A framework agnostic wrapper for SQLAlchemy that makes it really easy
to use by implementing a simple active record like api, while it still uses the db.session underneath

:copyright: © 2014/2016 by `Mardix`.
:license: MIT, see LICENSE for more details.

"""

from setuptools import setup

NAME = "Active-Alchemy"
py_module = "active_alchemy"
__version__ = '0.10.0'
__author__ = "Mardix"
__license__ = "MIT"
__copyright__ = "2014/2016 - Mardix"

setup(
    name=NAME,
    version=__version__,
    license=__license__,
    author=__author__,
    author_email='mardix@pylot.io',
    description=__doc__,
    long_description=__doc__,
    url='http://github.com/mardix/active-alchemy/',
    download_url='http://github.com/mardix/active-alchemy/tarball/master',
    py_modules=[py_module],
    install_requires=[
        "SQLAlchemy==1.0.12",
        "PyMySQL==0.6.6",
        "pg8000==1.10.2",
        "Paginator",
        "inflection==0.3.1"
    ],
    keywords=['sqlalchemy', 'flask', 'active sqlalchemy', 'orm', 'active record',
              'mysql', 'postgresql', 'pymysql', 'pg8000', 'sqlite'],
    platforms='any',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: PyPy',
    ]
)
