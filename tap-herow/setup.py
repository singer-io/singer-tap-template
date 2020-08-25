#!/usr/bin/env python
from setuptools import setup

setup(
    name="tap-herow",
    version="0.1.0",
    description="Singer.io tap for extracting data",
    author="Stitch",
    url="http://singer.io",
    classifiers=["Programming Language :: Python :: 3 :: Only"],
    py_modules=["tap_herow"],
    install_requires=[
        "singer-python>=5.0.12",
        "requests",
    ],
    entry_points="""
    [console_scripts]
    tap-herow=tap_herow:main
    """,
    packages=["tap_herow"],
    package_data = {
        "schemas": ["tap_herow/schemas/*.json"]
    },
    include_package_data=True,
)
