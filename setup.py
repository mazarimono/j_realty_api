from setuptools import setup, find_packages

setup(
    name='prop_api',
    version=0.1,
    packages=find_packages(),
    install_requires=[
        'pandas',
        'requests'
    ],
    include_package_data=True
)