#!/usr/bin/env python
"""The setup script."""

from setuptools import setup

with open("README.md", "r") as f:
    readme = f.read()

setup(
    name="aiosyncthing",
    version="0.5.1",
    author="Gleb Sinyavskiy",
    author_email="zhulik.gleb@gmail.com",
    description="Asynchronous Python client for the Syncthing REST API",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/zhulik/aiosyncthing",
    license="The MIT License",
    install_requires=["aiohttp>=3.7.4", "yarl>=1.6.3"],
    packages=["aiosyncthing"],
    package_dir={"aiosyncthing": "aiosyncthing"},
    include_package_data=True,
    zip_safe=True,
    keywords="syncthing,sync,rest,backup,api,aio,async,await",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: System :: Archiving :: Mirroring",
    ],
)
