#!/usr/bin/env/python2.7

from setuptools import setup

# Create the database (just importing will run it)
import create_db

# Install the Python app
# TODO: test this actually works -- this won't have a build, can it run from src?
setup(
    name             = 'Hextech Project X',
    version          = '1.0.0',
    author           = 'Benjamin David Holmes',
    author_email     = 'benjamin.holmes@imagini.net',
    url              = 'https://hextechprojectx.com',
    description      = 'Displays odds for League of Legends featured games.',
    py_modules       = ['hextech_project_x'],
    package_dir      = {'': 'src'},
    long_description = open( "readme.md" ).read(),
	install_requires = ['Flask', 'SQLAlchemy', 'MySQL-python', 'Flask-SQLAlchemy'],
	tests_require 	 = ['mock'],
    classifiers 	 = [
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Flask',
		'Intended Audience :: End Users/Desktop',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Topic :: Games/Entertainment',
		'Topic :: Games/Entertainment :: Real Time Strategy',
		'Topic :: Games/Entertainment :: Role-Playing',
		'Topic :: Scientific/Engineering :: Information Analysis'
    ]
) 