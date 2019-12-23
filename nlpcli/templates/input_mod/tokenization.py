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

    def __call__(self,example_list,token_fields = [],expand_fn = {}):

        """
            :params example_list: [example] list
            :params token_fields:[{},] e.g.,{'text_a':['label1','label2']},'text_b']
             字典表示以key为基准进行expand
            :params expand_fn expand 的方法，当token_fields 中有字典结构的时候，对应的每一个value必须有对应的函数
        """
        if not token_fields:
            raise ValueError('token_fields can not be none')
        if isinstance(expand_fn,dict):
            raise ValueError('expand_fn must be a dict：{0}'.format(str(example_fn)))
        if expand_fn:
            for k,v in example_fn.items():
                if not callable(v):
                    raise ValueError('The value in example_fn musk be function: {0}'.format(expand_fn))
        single_fields = [] # 没有依赖的token字段
        bound_fields = [] # 有 bound 的字段，里面是一个字典

        for field in token_fields:
            if isinstance(field,dict):
                if len(field.keys())>1:
                    raise ValueError('Field have one more key: {0}'.format(str(field)))
                for bound_field in bound_fields.values():
                    if bound_field not in expand_fn:
                        raise ValueError('Field in value of dict must be in expand_fn: {0}'.format(str(field)))
                bound_fields.append(field)
            elif isinstance(field,str):
                single_fields.append(field)
            else:
                raise ValueError('Token_fields can only include str or dict: {0}'.format(str(field)))


        [self._tokenize_one_sample(e,single_fields,bound_fields,expand_fn) for e in example_list]


class Tokenizer(TokenizerBase):

    def __init__(self):

        self._tokenizer = self.get_tokenizer()
        DP.tokenizer = self._tokenizer
        if hasattr(self._tokenizer,'tokenize'):
            raise ValueError('tokenizer must have a tokenize method')

        # self._fields =  DP.fields
        # {% if task_type == "sl" -%}
        # self.tokenize_domain = DP.config['TaskInput']['TokenizeDomainHeader'] # label 依照哪一个进行token化
        # self.label = [f for f in self._fields if f.startswith('label_')]
        # 
        # if len(self.label)>1:
        #     raise ValueError('There are two or more fields start with "label_", which is not allow in sequence labeling')
        # self.tag_scheme =  DP.config['TaskInput']['TagScheme'] #
        # if self.tag_scheme not in ['BIO','BIOES']:
        #     raise ValueError('tag scheme must be BIO or BIOES, current scheme is {0}'.format(self.tag_scheme))
        # {% endif %}

    def _tokenize_one_sample(self,example,single_fields,bound_fields,expand_fn):

        """

        :param self:
        :param single_fields: 简单字段的token化
        :param bound_fields: 绑定的字段的token化
        :param expand_fn: 绑定的字段对应的函数
        :return:
        """
        # 单个字段直接进行token化
        for field in single_fields:
            example[field+'_tokenized'] = self._tokenizer.tokenize(example[field])
        # 绑定的字段进行token化
        for bound_field in bound_fields:
            k = bound_field.keys()[0]
            v = bound_field[k]
            # tokenized 初始化
            example[k+'_tokenized'] = []
            # 对应到的一个映射函数，方便对token之后的进行还原
            # 里面保存的是当前字的对应到token之后的start与end index
            example[k+'_mapping'] = []
            for i in v:
                example[i+'_tokenized'] = []
            _example = [example[k]] + [example[i] for i in v]
            # 逐个位置都进行token化
            current_index = 0
            for t in zip(*_example):
                v_domain = self._tokenizer.tokenize(t[0])
                example[k+'_tokenized'] += v_domain
                example[k+'_mapping'].append((current_index,current_index+len(v_domain)-1))
                current_index = current_index+len(v_domain)
                for k,i in enumerate(v):
                    example[i+'_tokenized'] += expand_fn[i](v_domain,t[k+1])


    # def _tokenize_sequence_labelling_one_sample(self,example,single_fields,bound_fields):
    #
    #
    #     example[self.tokenize_domain+'_tokenized'] = []
    #
    #     example[self.label+'_tokenized'] = []
    #     for feature,lable in zip([example[self.tokenize_domain],example[self.label]):
    #         feature_after_tokenize = self._tokenizer.tokenize(feature)
    #         example[self.tokenize_domain+'_tokenized'].append(feature_after_tokenize)
    #         if self.tag_scheme=='BIO':
    #             if lable in ['O','I']:
    #                 example[self.label+'_tokenized'] = [label]*len(feature_after_tokenize)
    #         elif self.tag_scheme=='BIOES'




    # def _tokenize_classification_one_sample(self,example):
    #
    #     """
    #     分类任务中的token化
    #     :return:
    #     """
    #     pass

if __name__ == '__main__':
    pass
