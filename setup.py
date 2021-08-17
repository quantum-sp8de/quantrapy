from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))

this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md')) as f:
    long_description = f.read()

about = {}
with open(os.path.join(here, 'quantralib', '__version__.py'), 'r') as f:
    exec(f.read(), about)

setup(
    name='quantralib',
    version=os.getenv('BUILD_VERSION', about['__version__']),
    description='Python library for the eos.io REST API and QRandom ecosystem',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='plageat',
    author_email='plageat90@gmail.com',
    url='https://github.com/AlexandrDedckov/quantrapy',
#    packages=find_packages(),
    packages=["quantralib"],
    test_suite='nose.collector',
    install_requires=[
        'requests',
        'base58>=1.0.3',
        'ecdsa',
        'colander',
        'pytz',
        'six',
        'pyyaml',
    ],
    entry_points={
        'console_scripts': [
            'validate_chain = quantralib.command_line:validate_chain',
            'quantrapy = quantralib.command_line:cleos',
            'pytesteos = quantralib.command_line:testeos',
        ],
    })
