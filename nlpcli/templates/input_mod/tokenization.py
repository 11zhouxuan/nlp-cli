#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : {{create_time}}
# @Author : by {{author_name}}
# @File : {{file_name}}
# @Email : {{email}}
"""
token化模块,除了用已经用的tokenizer,用户必须实现TokenizerBase中的get_tokenizer方法,
"""
import os
from loguru import logger
from ..core.dataprocessing import DataProcess
DP = DataProcess()
# try:
# {% if tokenizer_type == "bert" -%}
#     from tokennizers.tokenizer_by_bert import FullTokenizer as _tokenizer
#     _tokenizer = _tokenizer(DP.config['bert'])
# {% else %}
#     from tokennizers.
# {% endif %}
# except:
#     raise ImportError('请导入正确的tokenizer 或者自定义一个tokenizer')

class TokenizerBase():



    def get_tokenizer(self):

        """
        :return: tokenizer 对象,里面必须包含字典，类似bert等的实现方式
        """
        raise NotImplementedError()

    def __call__(self,example_list):

        """

        :param example_list:
        :param token_fields: 为空表示除了label都要进行token化
        :return:
        """

        [self._tokenize_one_sample(e) for e in example_list]


class Tokenizer(TokenizerBase):

    def __init__(self):

        self._tokenizer = self.get_tokenizer()
        self._fields =  DP.fields


    def _tokenize_sequence_labelling_one_sample(self,example):

        """
        :param example: token化一个样本
        :return:
        """
        for field in self._fields:
            if field == 'label':
                pass
            else:
                pass


    def _tokenize_classification_one_sample(self,example):

        """
        分类任务中的token化
        :return:
        """
        pass

if __name__ == '__main__':
    pass
