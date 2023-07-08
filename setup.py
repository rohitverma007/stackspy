from setuptools import setup, find_packages

setup(
    name="stackspy",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "secp256k1",
    ],
    author="Rohit Verma",
    author_email="rohitverma@live.ca",
    description="Python Library for the Stacks ecosystem",
    url="https://github.com/rohitverma007/stackspy",
    keywords="stacks python",
)