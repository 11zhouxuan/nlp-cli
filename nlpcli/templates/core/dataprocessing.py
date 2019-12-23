#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : {{create_time}}
# @Author : by {{author_name}}
# @File : {{file_name}}
# @Email : {{email}}
import threading
import json
import pickle
class DataProcess():

    def __new__(cls, *args, **kwargs):

        """
        构造单例模式，方便在多个文件中共享数据
        :param args:
        :param kwargs:
        :return:
        """
        _instance_lock = threading.Lock() # 保证线程安全
        if not hasattr(DataProcess,"_instance"):
            with DataProcess._instance_lock:
                if not hasattr(DataProcess,"_instance"):
                    DataProcess._instance = object.__new__(cls)
        return DataProcess._instance

    def __init__(self):
        pass
    def _load_json(self,path):

        """
        打开json文件
        :param path: json文件的路径
        :return:
        """
        with open(path,'r',encoding='utf-8') as f:
            return json.load(f)
    def _load_pkl(self,path):

        """
        导入pkl文件
        :param path: pkl 文件的路径
        :return:
        """
        with open(path,'rb') as f:
            return pickle.load(f)

    def get_feature_vocab(self):

        """
        或者字符的对应的字典
        :return:
        """
        self._VocabFilePath = self.config['TaskInput']['VocabFilePath']
        if self._VocabFilePath.endswith('.json'):
            self._vocab = self._load_json(self._VocabFilePath)
            if not isinstance(self._vocab,dict):
                raise ValueError('vocab must be a dict saved as a json file')
        elif self._VocabFilePath.endswith('.pkl'):
            self._vocab = self._load_pkl(self._VocabFilePath)
            if not isinstance(self._vocab,dict):
                raise ValueError('vocab must be a dict saved as a json file')
        else:
            raise ValueError('you have to implement get_feature_vocab method by yourself!')
        self._inv_vocab = {v:k for k ,v in self._vocab.items()} # 反向字典
    def get_label_map(self):

        """
        获取label_map
        :return:
        """
        self._LabelMapPath = self.config['TaskInput']['LabelMapPath']
        if self._LabelMapPath.endswith('.json'):
            self._label_map = self._load_json(self._LabelMapPath)
        elif self._LabelMapPath.endswith('.pkl'):
            self._label_map = self._load_pkl(self._LabelMapPath)
        else:
            raise ValueError('you have to implement get_label_map method by yourself!')
        self._inv_label_map = {v:k for k,v in self._label_map.items()}

    def token_to_ids(self,voc,fields = [],example_lists = []):

        """
        利用 字典voc将example中的制定fields转化为id
        :param voc: dict
        :param fields: list
        :param example_list: list
        :return:
        """
        if not fields:
            raise ValueError('field can not be none')
        if not example_lists:
            raise ValueError('example_lists can not be none')
        def _token_to_ids_one_example(e):

            """
            单个句子转化成id
            :param e:
            :return:
            """
            for field in fields:
                if field+'_tokenized' in e:
                    e[field + '_ids'] = [voc[i] for i in e[field+'_tokenized']]
                else:
                    e[field + '_ids'] = [voc[i] for i in e[field]]
        for example_list in example_lists:
            [_token_to_ids_one_example(e) for e in example_list]












if __name__ == '__main__':
    pass
