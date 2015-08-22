from setuptools import setup, find_packages


setup(
    name='stargate',
    version=0.1,
    packages = find_packages(exclude=['test'])
)
