#!/usr/bin/env python
import os

from setuptools import find_packages, setup

setup(
    name="road-traffic-equlibrium",
    version="0.0.1",
    description="Traffic asignment problem algorithms",
    long_description=open(
        os.path.join(os.path.abspath(os.path.dirname(__file__)), "README.md")
    ).read(),
    long_description_content_type="text/markdown",
    author="jimmeryn@gmail.com",
    packages=find_packages(),
)
