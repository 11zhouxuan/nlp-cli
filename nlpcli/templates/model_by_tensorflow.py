#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : {{create_time}}
# @Author : by {{author_name}}
# @File : {{file_name}}
# @Email : {{email}}
import os
abs_path_dir = os.path.dirname(__file__)
import numpy as np
from tqdm import tqdm
from core import DataProcess
import tensorflow as tf
DP = DataProcess()
logger = DP.logger

class Model():

    def __init__(self):
        self._config = DP.config
        self._set_droupout_var() # 设置相关的dropout参数
        self._set_inputs_and_label_var()
        self._build_model()

        # tensorflow 相关操作
        config = tf.ConfigProto()
        config.gpu_options.allow_growth = True
        self.sess = tf.Session(config = config)
        self.train_op = self._get_train_op()
        self._add_summary() # 可视化
        # 参数重建
        self._parameters_restore()
        
    def _set_dropout_var(self):

        """
        设置dropout相关参数,特别注意要区分训练的测试中的情况
        :return:
        """
        raise NotImplementedError()
    def _set_input_and_label_var(self):

        """
        设置输入与输出对应的变量
        :return:
        """
        raise NotImplementedError()

    def _add_summary(self):

        """
        增加训练中需要记录的tensor
        :return:
        """
        # 在 tf.summary.merge_all 之前可以添加想要记录的tensor
        self.merge_summary_op = tf.summary.merge_all()
        path_summary = os.path.join(self._config['TensorflowConfig']['PathSummary'],str(os.getpid()))
        if not os.path.exists(path_summary):
            os.mkdir(path_summary)
        self.train_writer = tf.summary.FileWriter(path_summary,self.sess.graph)
    def _parameters_restore(self):
        
        """
        参数重建,多用于预训练模型中
        :return: 
        """
        raise NotImplementedError()
    def _get_train_op(self):
        
        """
        得到训练的op
        :return: 
        """
        raise NotImplementedError()

    def _build_model(self):

        """
        模型的实现阶段
        :return:
        """

        raise NotImplementedError()

    def fit(self,data_train  = None, data_dev = None, data_test = None):

        """
        训练函数
        :param data_train:  训练集, 生成器
        :param data_dev: 验证集, 生成器
        :param data_test: 测试集, 生成器
        :return:
        """

        raise NotImplementedError()


    

if __name__ == '__main__':
    pass
