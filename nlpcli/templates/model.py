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
DP = DataProcess()
logger = DP.logger

class Model():

    def __init__(self):
        self._config = DP.config
        self._set_droupout_var() # 设置相关的dropout参数
        self._set_inputs_and_label_var()
        self._build_model()

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

    def _build_model(self):

        """
        模型的实现阶段
        :return:
        """
        raise NotImplementedError()

if __name__ == '__main__':
    pass
