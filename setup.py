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
    long_description_content_type='COMING SOON',
    url='https://github.com/garethwalkom/technopy',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'LICENSE :: OSI APPROVED :: GNU GENERAL PUBLIC LICENSE V3 (GPLV3)',
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
