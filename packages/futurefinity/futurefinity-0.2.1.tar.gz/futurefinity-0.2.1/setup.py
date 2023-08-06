#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#   Copyright 2016 Futur Solo
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import futurefinity

import sys

if not sys.version_info >= (3, 5, 1):
    raise RuntimeError("FutureFinity Requires Python 3.5.1 or higher.")

install_requires = []

full_requires = ["jinja2", "cryptography"]

tests_require = ["requests", "nose2"]
tests_require.extend(full_requires)

if __name__ == "__main__":
    setup(
        name="futurefinity",
        version=futurefinity.version,
        author="Futur Solo",
        author_email="futursolo@gmail.com",
        url="https://github.com/futursolo/futurefinity",
        license="Apache License 2.0",
        description="FutureFinity is an asynchronous Python web framework "
                    "designed for asyncio and native coroutines.",
        long_description=open("README.rst", "r").read(),
        packages=["futurefinity"],
        package_data={
            "futurefinity": ["README.rst", "LICENSE"]
        },
        test_suite="nose2.collector.collector",
        install_requires=install_requires,
        tests_require=tests_require,
        zip_safe=False,
        extras_require={
            "full": full_requires,
            "test": tests_require
        },
        classifiers=[
            "License :: OSI Approved :: Apache Software License",
            "Operating System :: MacOS",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft",
            "Operating System :: Microsoft :: Windows",
            "Operating System :: POSIX",
            "Operating System :: POSIX :: Linux",
            "Operating System :: Unix",
            "Programming Language :: Python",
            "Programming Language :: Python :: 3 :: Only",
            "Programming Language :: Python :: Implementation :: CPython"
        ]
    )
