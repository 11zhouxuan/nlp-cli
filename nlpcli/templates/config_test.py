#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/11/23 10:55 
# @Author : by 周旋 
# @File : config_test.py 
# @Software: PyCharm
# plt.switch_backend('Qt5Agg')
import os
from jinja2 import Template
import yaml
with open('config.yml','r',encoding='utf-8') as f:
    config = f.read()
print(config)
template = Template(config)

r_render =  template.render(**{"task_type" : "sl","project_name" :"zx"})

with open('config_after_render.yml','w',encoding='utf-8') as f:
    f.write(r_render)
with open('config_after_render.yml','r',encoding='utf-8') as file_config:
    config = yaml.load(file_config)
print(config)
SentencesDelimiter = config['TaskInput']['SentencesDelimiter']
print('\nsdf\n'.split(SentencesDelimiter))

if __name__ == '__main__':
    pass
