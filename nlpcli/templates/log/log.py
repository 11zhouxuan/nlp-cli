#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : {{create_time}}
# @Author : by {{author_name}}
# @File : train.py
# @Email : {{email}}
"""
日志配置模块,提供两种方式,
1.自带的logging
2.第三方的loguru(控制台更加好看)
日志将保存两份,一份是info级别，一份是debug级别
分别保存到两个txt文件中
"""
import os
import sys
try:
    from loguru import logger
    loguru_format ='<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <b>process_id: {process}</b> | <level>{level}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>'
    logger.remove(0) # 去掉自带的logger,防止窗口打印出来的与写入文本的不一致
except:
    import logging
    logging_format = "%(asctime)s |process_id: %(process)d | %(levelname)s | %(filename)s: %(funcName)s :%(lineno)d -  %(message)s"
import time
abs_path_dir = os.path.dirname(__file__)
if not os.path.exists(abs_path_dir + "/log_debug"):
    os.mkdir(abs_path_dir + "/log_debug")
if not os.path.exists(abs_path_dir + "/log_info"):
    os.mkdir(abs_path_dir + "/log_info")

__author_name__ = "_".join("{{author_name}}".strip().split()) # 处理作者名称
path_debug = abs_path_dir + f"/log_debug/{__author_name__}_{os.getpid()}_time_{time.strftime('%Y-%m-%d_%H-%M-%S')}.log"
path_info = abs_path_dir + f"/log_info/{__author_name__}_{os.getpid()}_time_{time.strftime('%Y-%m-%d_%H-%M-%S')}.log"


def get_logger(file_name = '', level = 0):

    # 输入到文件
    fileHandle = logging.FileHandler(file_name,'a',encoding="utf-8")
    fmt = logging.Formatter(fmt = logging_format)
    fileHandle.setFormatter(fmt)
    # 输入到控制台
    consoleHandle = logging.StreamHandler()
    consoleHandle.setFormatter(fmt)

    # 定义日志
    logger = logging.Logger(__author_name__,level=level)
    logger.addHandler(fileHandle)
    logger.addHandler(consoleHandle)
    return logger


if 'loguru_format' in locals():
    logger.add(sys.stderr,level=0,format = loguru_format)
    logger.add(path_info,encoding = 'utf-8',level='INFO',format=loguru_format)
    logger.add(path_debug,encoding = 'utf-8',level='DEBUG',format=loguru_format)
    # logger.add(sys.stdout,encoding = 'utf-8',level= 0,format=loguru_format)
else:
    # TODO 目前logging的日志只能保存一个INFO级别的信息
    logger = get_logger(path_info,level=20)


if __name__ == '__main__':
    logger.debug('sg')
