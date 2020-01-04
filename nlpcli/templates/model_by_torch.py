#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : {{create_time}}
# @Author : by {{author_name}}
# @File : {{file_name}}
# @Email : {{email}}
from core import DataProcess
from tqdm import tqdm
import numpy as np
import os
abs_path_dir = os.path.dirname(__file__)
DP = DataProcess()
logger = DP.logger


class Model():

    def __init__(self):
        self._config = DP.config
        self._set_droupout_var()  # 设置相关的dropout参数
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
