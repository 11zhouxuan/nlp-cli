#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : {{create_time}}
# @Author : by {{author_name}}
# @File : train.py
# @Email : {{email}}
import os
import yaml
from log.log import logger
from auto_device import get_max_remain_gpu
def main(**kwargs)
    with open('config.yml') as file_config:
        config = yaml.load(file_config)
    cuda_id = get_max_remain_gpu()


if __name__ == '__main__':
    pass
