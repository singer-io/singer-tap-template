#!/usr/bin/env python
from setuptools import setup, find_packages

setup(name="{{cookiecutter.project_name}}",
      version="0.1.0",
      description="Singer.io tap for extracting data from the Jira API",
      author="Stitch",
      url="http://singer.io",
      classifiers=["Programming Language :: Python :: 3 :: Only"],
      py_modules=["{{cookiecutter.project_slug}}"],
      install_requires=[
          "singer-python>=3.2.0",
          "requests",
          "backoff",
          "attrs",
      ],
      entry_points="""
          [console_scripts]
          {{cookiecutter.project_name}}={{cookiecutter.project_slug}}:main
      """,
      packages=["{{cookiecutter.project_slug}}"],
      package_data = {
          "schemas": ["{{cookiecutter.project_slug}}/schemas/*.json"]
      },
      include_package_data=True,
)
