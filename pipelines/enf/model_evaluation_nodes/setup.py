#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from setuptools import setup, find_packages

setup(
    name="ai_model_monitoring",
    version="1.0",
    packages=find_packages(),
    include_package_data=True,
    author="punchplatform",
    author_email="contact@punchplatform.com",
    description="custom node for ai model monitoring",
    python_requires='>=3.6',
    install_requires=[
        "pex==2.1.6",  # this is important do not remove
        "requests==2.24.0",  # this is important do not remove
        "numpy==1.19.1",
        "pandas==1.1.2",
        "py4j==0.10.9",
        "python-dateutil==2.8.1",
        "pytz==2020.1",
        "six==1.15.0"   
    ]
)
