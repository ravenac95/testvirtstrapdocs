"""
VirtStrap
=========

A bootstrapping mechanism for virtualenv, buildout, and shell scripts.
"""
from setuptools import setup, find_packages

setup(
    name="VirtStrap",
    version="0.1",
    license="MIT",
    author="Reuven V. Gonzales",
    url="http://tobetter.us",
    author_email="reuven@tobetter.us",
    description="A simple boostrapping mechanism for virtualenv, buildout and shell scripts",
    packages=find_packages(exclude=['tests', 'tests.*']),
    zip_safe=False,
    platforms='*nix',
    install_requires=[
        "PasteScript>=1.3",
    ],
    entry_points="""
        [paste.paster_create_template]
        virtstrap_basic = virtstrap.entry.template:VirtStrapBasicTemplate
    """,
    classifiers = [
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
)


