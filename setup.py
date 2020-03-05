# -*- coding: utf-8 -*-

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='technopy',
    version='0.0.1',
    author='Gareth V. Walkom',
    author_email='walkga04@googlemail.com',
    description='technopy allows you to control your TechnoTeam Luminance Camera or Hyperspectral Camera.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/garethwalkom/technopy',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
