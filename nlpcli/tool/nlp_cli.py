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
import traceback
# 文件名称索引
choice_to_file = {
    'tensorflow': 'model_by_tensorflow.py',
    'torch': 'model_by_torch.py',
    'none': 'model.py'
}

path_templates = os.path.join(os.path.dirname(nlpcli.__file__), 'templates')
# path_templates = "E:\\pycharm\\NLP-cli\\nlpcli\\templates"


def parse_args():
    parser = argparse.ArgumentParser(
        prog='nlp-cli',
        description='use nlp-cli command to construct a scaffold of special NLP task')
    parser.add_argument(
        '-t',
        '--task_type',
        required=True,
        type=str,
        choices=[
            'sl',
            'tc',
            'qa'])
    args = vars(parser.parse_args())  # 将参数转换成字典
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
    args['email'] = author_email

    tokenizer_type_choices = ['bert', 'ernie', 'xlnet', 'none']
    while True:
        tokenizer_type = input(f"tokenizer type, choices:  {'  '.join([str(i)+'. '+ str(k) for i,k in enumerate(tokenizer_type_choices)])}, (it is can be constom if none is choosed) \n")
        if tokenizer_type in tokenizer_type_choices:
            args['tokenizer_type'] = tokenizer_type
            break
        if tokenizer_type in [
            str(i) for i in range(
                len(tokenizer_type_choices))]:
            args['tokenizer_type'] = tokenizer_type_choices[int(
                tokenizer_type)]
            break
        print('The tokenizer type mush be in choices, please re-enter')

    # 构建模型支持的计算库格式
    model_construct_choices = ['tensorflow', 'torch', 'none']
    while True:
        model_construct_type = input(f"model construction, choices:  {'  '.join([str(i)+'. '+ str(k) for i,k in enumerate(model_construct_choices)])}, (it is can be constom if none is choosed)\n")
        if model_construct_type in model_construct_choices:
            args['model_construct_type'] = model_construct_type
            break
        if model_construct_type in [
            str(i) for i in range(
                len(model_construct_choices))]:
            args['model_construct_type'] = model_construct_choices[int(
                model_construct_type)]
            break

        print('The model construction mush be in choices, please re-enter')

    args['create_time'] = time.strftime("%Y/%m/%d %H:%M", time.localtime())

    distribute_from_templates(args)


def distribute_from_templates(args):
    """
    利用文件夹work进行模版渲染
    :param args: 前端穿进来的各种参数
    :return:
    """
    def _render_one_file(path_sorce, path_target, args):
        try:
            with open(path_sorce, 'r', encoding='utf-8') as f:
                r = f.read()
            template = Template(r)
            r_render = template.render(**args)
            with open(path_target, 'w', encoding='utf-8') as f:
                f.write(r_render)
        except BaseException:
            print(traceback.print_exc())
            print('当前渲染出错的路径', path_sorce, path_target)
            print(sg)
    # 创建项目的跟目录
    path_project = os.path.join(os.getcwd(), args['project_name'])
    if os.path.exists(path_project):
        raise ValueError('the project path  already exists')
    os.mkdir(path_project)
    # 建立相关文件夹并逐个渲染文件
    for root, dirs, files in os.walk(path_templates):
        print('当前root', root)

        if "__pycache__" in root:
            continue
        # 建立文件夹
        for name in dirs:
            if "__pycache__" in name:
                continue
            ori_path = os.path.join(root, name)
            new_path = path_project + ori_path.replace(path_templates, '')
            os.mkdir(new_path)

        # 渲染文件
        for name in files:
            ori_name = name
            new_name = name

            # model 特殊文件名称操作
            if name.startswith('model'):

                if choice_to_file[args['model_construct_type']] != ori_name:
                    continue
                new_name = 'model.py'

            # 单个文件进行渲染
            ori_path = os.path.join(root, ori_name)
            new_path = path_project + ori_path.replace(path_templates, '')
            new_path = new_path.replace(ori_name, new_name)  # 名字替换一下

            args['file_name'] = new_name

            _render_one_file(ori_path, new_path, args)


if __name__ == '__main__':
    parse_args()
