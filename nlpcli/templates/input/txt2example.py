#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : {{create_time}}
# @Author : by {{author_name}}
# @File : train.py
# @Email : {{email}}
"""
txt to [example]
"""
from collections import namedtuple

sentence_delimiter = {
    'sl':'\n\n',
    'qa':'\n',
    'tc':'\n'
}
class Example(dict):
    pass

class LoadTxt():

    def __init__(self,task_type,path_txt,do_predict = False):

        """

        :param task_type: str
        :param path_txt: str
        :param do_predict: bool 可以允许一列数据
        """
        self._task_type = task_type
        self._path_txt = path_txt
        self._do_predict = do_predict

        self._parse_sentence_delimiter()

        self._sentences = self.load_txt_as_sentences()

        self.attributes = self.get_attributes()
    def _parse_sentence_delimiter(self):

        if self._task_type in sentence_delimiter:
            self._sentences_delimiter = sentence_delimiter[self._task_type]
        else:
            raise ValueError('error task type: {0}'.format(self._task_type))

    def load_txt_as_sentences(self):

        with open(self._path_txt,'r',encoding='utf-8') as f:
            sentences = f.read().split(self._sentences_delimiter)
        return sentences

    def get_attributes(self):

        """
        通过第一行得到文本的属性值,没有属性的用[text_1,...,text_N,label] 代替
        同时获取当前文本列之间的分隔符
        :return:
        """

        line_0 = self._sentences[0]
        def _get_delimiter():

            if len(line_0.split('\t'))>1:
                self._delimiter = '\t'
            elif len(line_0.split(' '))>1:
                self._delimiter = ' '
            elif self._do_predict:
                self._delimiter = ' '
            else:
                raise ValueError('delimiter between columns can only by \\t or " "')

        _get_delimiter()
        line_0 = line_0.split(self._delimiter)
        if 'text_a' == line_0[0] and 'label' == line_0[-1]:
            attributes = line_0
            self._sentences.pop[0] # 此时去掉第一行
        else:
            if self._do_predict:
                attributes = ['text_{0}'.format(i+1) for i in range(len(line_0)-1)]
            else:
                attributes = ['text_{0}'.format(i+1) for i in range(len(line_0)-1)] + ['label']
        return attributes


    def sentence2examples(self):

        """
        将句子转化成对应的example
        这里处理的时候不需要区分任务
        :return:
        """
        # 去掉空的句子，一般为最后一个句子
        self._sentences = [s for s in self._sentences if s]

        def _one_sentence_to_example(sentence,guid):

            lines = sentence.split('\n') # 对于分类等任务就只有一行

            lines = [line.split(self._delimiter) for line in lines]

            lines_by_attributes = list(zip(*lines))
            e = Example()
            for k,attr in enumerate(self.attributes):
                e[attr] = lines_by_attributes[k]
            e['guid'] = guid
            return e
        examples = list(map(_one_sentence_to_example,self._sentences,list(range(len(self._sentences)))))

        return examples


if __name__ == '__main__':
    pass
