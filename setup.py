#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='humio',
    version='0.1',
    author='Jeppe Bronsted',
    author_email='',
    description='CLI tool for accessing Huio',
    url='https://cloud.humio.com',
    packages=find_packages(exclude=['*.tests']),
    install_requires=['requests', 'docopt'],
    entry_points={
        'console_scripts': [
            'humio = humio_client:main',
        ]
    }
)
