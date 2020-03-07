# -*- coding: utf-8 -*-

from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('technopy/requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='technopy',
    version='0.0.11',
    author='Gareth V. Walkom',
    author_email='walkga04@googlemail.com',
    license='GPLv3',
    description='technopy allows you to control your TechnoTeam Luminance Camera or Hyperspectral Camera.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/garethwalkom/technopy',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
