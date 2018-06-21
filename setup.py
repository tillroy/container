from setuptools import setup, find_packages

import container


setup(
    name="container",
    version=container.__version__,
    # packages=find_packages(exclude=["tests"]),
    packages=find_packages(),
    author='Roman Peresoliak',
    author_email='roman.peresoliak@gmail.com',
    include_package_data=True,

    # package_data={
        # If any package contains *.txt or *.rst files, include them:
        # "": ["*.json"],
    # },

    install_requires=[
        "ujson>=1.35",
        ]
)
