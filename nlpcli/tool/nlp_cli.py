#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/11/13 20:10 
# @Author : by 周旋 
# @File : nlp_cli.py 
# @Software: PyCharm
# plt.switch_backend('Qt5Agg')

import argparse
import os

def parse_args():
    parser = argparse.ArgumentParser(prog='nlp-cli', description='use nlp-cli command to construct a scaffold of special NLP task')
    parser.add_argument('-t','--task_type', required=True, type=str,choices = ['sl','tc','qa'])
    args = parser.parse_args()
    print(type(args))
    print(args)



if __name__ == '__main__':

    parse_args()
