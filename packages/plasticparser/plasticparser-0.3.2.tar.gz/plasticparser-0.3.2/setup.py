# -*- coding: utf-8 -*-

from distutils.core import setup

long_description = """
 Let's to convert Google Like Query Language into
 ElasticSearch understandable Query DSL
 """

setup(
    name='plasticparser',
    version='0.3.2',
    description='An Elastic Search Query Parser',
    long_description=long_description,
    url='https://github.com/Aplopio/plasticparser',
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 2.7",
    ],
    keywords=[
        "elasticsearch ", "query language", "query parser"
    ],
    packages=['plasticparser'],
    install_requires=[
        'pyparsing==2.0.2',
        'ProxyTypes==0.9'
    ],
)
