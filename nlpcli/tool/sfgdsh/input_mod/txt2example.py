#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/12/24 19:23
# @Author : by dh
# @File : txt2example.py
# @Email : 
"""
txt to [example]
"""
import os
from loguru import logger
from ..core.dataprocessing import DataProcess
from collections import defaultdict
DP = DataProcess()

class Example(defaultdict(list)):
    pass

class LoadTxt():

    def __init__(self):

        """
        :param task_type: str
        :param path_txt: str
        :param do_predict: bool 可以允许一列数据
        """
        self._get_config_from_dp()

    def _get_config_from_dp(self):
        """
        从 dataprocess 中获取配置
        :param self:
         :return:
        """
        self._is_sl_task = True if DP.config['task_type'] =='sl' else False
        self._has_header = True if DP.config['TaskInput']['TextHasHeaders'] else False
        self._SentencesDelimiter = DP.config['TaskInput']['SentencesDelimiter']
        self._ColumnDelimiter = DP.config['TaskInput']['ColumnDelimiter']
        if self._is_sl_task:
            self._CharacterDelimiter = DP.config['TaskInput']['CharacterDelimiter']
            if self._CharacterDelimiter==self._ColumnDelimiter:
                raise ValueError(f'字符分隔符与列分隔符相等了, {self._CharacterDelimiter}={self._ColumnDelimiter}')

        # 解析列
        self._col2field = {v:k for k,v in DP.config['TextHeaders'] if v}
        # TODO 检查列指标是否符合要求
        DP.fields = self._col2field.values()

    def load_txt_as_sentences(self):

        if not self._SentencesDelimiter:
            raise ValueError(f'SentencesDelimiter is {self._SentencesDelimiter}')

        with open(self._path_txt,'r',encoding='utf-8') as f:
            sentences = f.read().split(self._SentencesDelimiter)
        return sentences

    def sentence2examples(self):

        """
        将句子转化成对应的example
        这里处理的时候不需要区分任务
        :return:
        """
        if self._is_sl_task and not self._CharacterDelimiter:
            raise ValueError(f'序列标注任务必须有字符分隔符,当前字符分隔符为{self.__CharacterDelimiter}')
        if not self._ColumnDelimiter:
            raise ValueError(f'列之间不能没有标志符,当前为：{str(self._ColumnDelimiter)}')
        # 去掉空的句子，和表头
        if self._has_header:
            self._sentences.pop(0)
        self._sentences = [s for s in self._sentences if s]

        logger.info(f'{self._txt_name}中去掉空字符串或者表头之后的样本个数: {len(self._sentences)}')

        def _one_sentence_to_example(sentence,guid):

            attrs = sentence.split(self._ColumnDelimiter)

            e = Example()
            for k,attr in enumerate(attrs):
                if k in self._col2field:
                    if self._is_sl_task:
                        attr = attr.split(self._CharacterDelimiter)
                    e[self._col2field[k+1]] = [attr]
            e['guid'] = str(self._txt_name) + '_' + str(guid)
            return e

        examples = list(map(_one_sentence_to_example,self._sentences,range(len(self._sentences))))

        return examples

    def __call__(self,path_txt):

        self._txt_name = os.path.basename(path_txt).split('.')[0]
        self._path_txt = path_txt

        self._sentences = self.load_txt_as_sentences()

        example_list = self.sentence2examples()

        return example_list



if __name__ == '__main__':
    pass