#!/usr/bin/env/python2.7

import subprocess

# Run python tests
subprocess.Popen(['nosetests'])

# Run JS tests
subprocess.Popen(['node', 'node_modules/karma/bin/karma', 'start', '--single-run'])
