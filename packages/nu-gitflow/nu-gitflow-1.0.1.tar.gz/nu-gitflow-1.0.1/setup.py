#!/usr/bin/env python
#
# This file is part of `gitflow`.
# Copyright (c) 2010-2011 Vincent Driessen
# Copyright (c) 2012-2013 Hartmut Goebel
# Copyright (c) 2015 Christian Assing
# Distributed under a BSD-like license. For full terms see the file LICENSE.txt
#

import codecs
try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

import gitflow as distmeta

long_description = codecs.open('README.rst', "r", "utf-8").read()

install_requires = ['GitPython>=1.0.1', "future"]

setup(
    name="nu-gitflow",
    version=distmeta.__version__,
    description="Git extensions to provide high-level repository operations for Vincent Driessen's branching model.",
    author=distmeta.__author__,
    author_email=distmeta.__contact__,
    url=distmeta.__homepage__,
    platforms=["any"],
    license="BSD",
    packages=find_packages(exclude=("tests*",)),
    install_requires=install_requires,
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'git-flow = gitflow.bin:main'
        ]
    },
    classifiers=[
        # Picked from
        #    http://pypi.python.org/pypi?:action=list_classifiers
        # "Development Status :: 1 - Planning",
        # "Development Status :: 2 - Pre-Alpha",
        # "Development Status :: 3 - Alpha",
        # "Development Status :: 4 - Beta",
        "Development Status :: 5 - Production/Stable",
        # "Development Status :: 6 - Mature",
        # "Development Status :: 7 - Inactive",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Operating System :: POSIX",
        "Operating System :: MacOS :: MacOS X",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Topic :: Software Development :: Version Control",
    ],
    long_description=long_description,
)
