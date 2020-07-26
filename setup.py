#!/usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name="aiosyncthing",
    version="2.4.2",
    author="Gleb Sinyavskiy",
    author_email="zhulik.gleb@gmail.com",
    description="Async Python bindings to the Syncthing REST interface",
    url="https://github.com/zhulik/aiosyncthing",
    license="The MIT License",
    install_requires=["aiohttp==3.6.1", "yarl=1.5.0"],
    packages=["aiosyncthing"],
    package_dir={"aiosyncthing": "aiosyncthing"},
    include_package_data=True,
    zip_safe=True,
    keywords="syncthing,sync,rest,backup,api,aio,async,await",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: System :: Archiving :: Mirroring",
    ],
)
