#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from setuptools import setup, find_packages

setup(
    name="nodes",
    version="1.0",
    packages=find_packages(),
    include_package_data=True,
    author="punchplatform",
    author_email="contact@punchplatform.com",
    description="boilerplate for custom nodes",
    python_requires='>=3.6',
    install_requires=[
        "pex==2.1.6",  # this is important do not remove
        "requests==2.24.0",  # this is important do not remove
        "mlflow==1.8.0",
        "pandas==1.1.5",
        "numpy==1.19.5",
        "scikit-learn==0.23.2"
    ]
)