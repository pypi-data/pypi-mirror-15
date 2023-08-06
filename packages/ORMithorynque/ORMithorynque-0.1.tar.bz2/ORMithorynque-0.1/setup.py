#! /usr/bin/env python
# -*- coding: utf-8 -*-
# ORMithorynque
# Copyright (C) 2016 Jean-Baptiste LAMY

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import os, os.path, sys, glob

HERE = os.path.dirname(sys.argv[0]) or "."

if len(sys.argv) <= 1: sys.argv.append("install")


import distutils.core, distutils.sysconfig
if ("upload_docs" in sys.argv) or ("build_sphinx" in sys.argv): import setuptools


distutils.core.setup(
  name         = "ORMithorynque",
  version      = "0.1",
  license      = "LGPLv3+",
  description  = "ORMithorynque is an ORM (Object Relational Mapper) for Python and SQLite3 with excellent performances and multiple inheritance support.",
  long_description = open(os.path.join(HERE, "README.rst")).read(),
  
  author       = "Lamy Jean-Baptiste (Jiba)",
  author_email = "jibalamy@free.fr",
  url          = "https://bitbucket.org/jibalamy/ormithorynque",
  classifiers  = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "Intended Audience :: Information Technology",
    "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: Implementation :: PyPy",
    "Topic :: Database",
    ],
  
  package_dir  = {"ormithorynque" : "."},
  packages     = ["ormithorynque"],
#  package_data = {"ormithorynque" : []}
  )
