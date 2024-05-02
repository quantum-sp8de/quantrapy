#!/bin/bash

sudo apt-get install python3-all python-all dh-python python3-stem python3-stdeb -y

DIRA=$(dirname "$0")

pushd $DIRA/../../
rm -rf deb_dist/
rm -rf dist/
python3 setup.py --command-packages=stdeb.command sdist_dsc --depends3='python3-colander' --depends3='qrng-chip-converter'
cd $(ls -d deb_dist/quantralib-*/)
dpkg-buildpackage -rfakeroot -uc -us
popd
