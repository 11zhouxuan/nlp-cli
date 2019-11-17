#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/11/13 20:10 
# @Author : by 周旋 
# @File : nlp_cli.py 



import argparse
import os
from jinja2 import Template
import nlpcli
import time
path_templates = os.path.join(os.path.dirname(nlpcli.__file__),'templates')
def parse_args():
    parser = argparse.ArgumentParser(prog='nlp-cli', description='use nlp-cli command to construct a scaffold of special NLP task')
    parser.add_argument('-t','--task_type', required=True, type=str,choices = ['sl','tc','qa'])
    args = vars(parser.parse_args()) # 将参数转换成字典
    # 增加其他必要参数
    while True:
        project_name = input('project name: ')
        if project_name:
            args['project_name'] = project_name
            break
        else:
            print('Project name cannot be empty, please re-enter ')
    author_name = input('author name: ')
    args['author_name'] = author_name

    author_email = input('author email: ')
    args['author_email'] = author_email

    args['create_time'] = time.strftime("%Y/%m/%d %H:%M", time.localtime())

    distribute_from_templates(args)
def distribute_from_templates(args):

    """
    从模版文件处进行分发
    :param args:
    :return:
    """
    path_project = os.path.join(os.getcwd(),args['project_name'])
    if os.path.exists(path_project):
        raise ValueError('the project path  already exists')
    os.mkdir(path_project)
    def _render_one_file(path_sorce,path_target):

        with open(path_sorce,'r',encoding='utf-8') as f:
            r = f.read()
        template = Template(r)
        r_render =  template.render(**args)
        with open(path_target,'w',encoding='utf-8') as f:
            f.write(r_render)

    _render_one_file(os.path.join(path_templates,"__init__.py"),os.path.join(path_project,"__init__.py"))
    # 处理config文件
    _render_one_file(os.path.join(path_templates,'config.yml'),os.path.join(path_project,'config.yml'))

    # 处理log文件
    _render_one_file(os.path.join(path_templates,'log.py'), os.path.join(path_project,'log.py'))

    # 处理input文件
    os.mkdir(os.path.join(path_project,'input'))
    _render_one_file(os.path.join(path_templates,'input','__init__.py'),os.path.join(path_project,'input','__init__.py'))
    _render_one_file(os.path.join(path_templates,'input','DataProcessing.py'),os.path.join(path_project,'input','DataProcessing.py'))
    _render_one_file(os.path.join(path_templates,'input','txt2example.py'),os.path.join(path_project,'input','txt2example.py'))

    # 处理model文件
    _render_one_file(os.path.join(path_templates,'model','model.py'),os.path.join(path_project,'model.py'))

    # 处理train文件
    _render_one_file(os.path.join(path_templates,'train','train.py'),os.path.join(path_project,'train.py'))

    # 处理predict文件
    _render_one_file(os.path.join(path_templates,'predict','predict.py'),os.path.join(path_project,'predict.py'))















if __name__ == '__main__':

    parse_args()
