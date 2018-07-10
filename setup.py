#!/usr/bin/env python
# coding: utf-8

# Copyright (c) 2017, Zebula Sampedro, CU Boulder Research Computing.
# Distributed under the terms of the Modified BSD License.

# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

from __future__ import print_function

import os
import sys

from distutils.core import setup

pjoin = os.path.join
here = os.path.abspath(os.path.dirname(__file__))

# Get the current package version.
version_ns = {}
with open(pjoin(here, 'version.py')) as f:
    exec(f.read(), {}, version_ns)

setup_args = dict(
    name                = 'optionsspawner',
    packages            = ['optionsspawner'],
    version             = version_ns['__version__'],
    description         = """Options Form Spawner: Mixins and utilities for adding options forms with validation to JupyterHub spawners.""",
    long_description    = "",
    author              = "Zebula Sampedro",
    author_email        = "sampedro@colorado.edu",
    url                 = "https://github.com/ResearchComputing/jupyterhub-options-spawner",
    license             = "BSD",
    platforms           = "Linux",
    keywords            = ['Interactive', 'Interpreter', 'Shell', 'Web', 'Jupyter', 'JupyterHub'],
    classifiers         = [
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
)

# setuptools requirements
if 'setuptools' in sys.modules:
    setup_args['install_requires'] = install_requires = []
    with open('requirements.txt') as f:
        for line in f.readlines():
            req = line.strip()
            if not req or req.startswith(('-e', '#')):
                continue
            install_requires.append(req)


def main():
    setup(**setup_args)

if __name__ == '__main__':
    main()
