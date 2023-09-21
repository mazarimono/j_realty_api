from setuptools import setup, find_packages

setup(
    name='j_realty_api',
    version=0.1,
    packages=find_packages(),
    install_requires=[
        'pandas',
        'requests'
    ],
    include_package_data=True
)