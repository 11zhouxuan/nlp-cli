#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/11/13 19:50
# @Author : by zhou xuan
# @File : setup.py
# @Software: PyCharm
# plt.switch_backend('Qt5Agg')
import os
from setuptools import setup,find_packages
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname), encoding='utf-8').read()
setup(
    name = 'nlpcli',
    version = '1.0',
    author = 'Zhou Xuan',
    author_email = '15110180025@fudan.edu.cn',
    description = 'A scaffold for several NLP tasks',
    packages = find_packages(where='.', exclude=(), include=('*',)),
    long_description = read('README.md'),
    install_requires=[
        'jinja2',
        'pyyaml'
    ],
    license = 'MIT',
    python_requires = '>=3.5',
    entry_points = {
        'console_scripts' : [
            'nlp-cli = nlpcli.tool.nlp_cli:parse_args'
        ]
    }
)
