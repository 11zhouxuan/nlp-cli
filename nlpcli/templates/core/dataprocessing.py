#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : {{create_time}}
# @Author : by {{author_name}}
# @File : {{file_name}}
# @Email : {{email}}
import threading
import json
import pickle
import os
import datetime
import shutil

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
        self._current_train_epoch = 0
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


    def _example_serializer(self, exexample_list,file_name = ''):

        """
        将example序列化
        写入的规则每一个example先用pickle序列化,然后再已行行写到文本里去
        :param exexample_list: [example1,example2,...]
        :param file_name: 保存的名称
        :return:
        """
        with open(file_name,'wb') as f:
            f.write(b'\n'.join([pickle.dumps(e) for e in exexample_list]))
    def _example_inverse_serializer(self,file_handle):

        """
        :param file:
        :return:
        """
        lines = file_handle.readlines()
        examples = [pickle.loads(line) for line in lines]
        file_handle.close()
        return examples

    def _example_inverse_serializer_by_batch(self,file_handle,batch_size = 16,is_train = True):

        """
        逐个batch进行反序列化
        :param file_handle: 文件句柄
        :param batch_size: int
        :param is_train: train 要进行循环
        :return:
        """
        examples = []
        while batch_size:
            try:
                line = next(file_handle)
                e = pickle.loads(line)
                examples.append(e)
            except StopIteration:
                # 循环到底了
                if is_train:
                    self._current_train_epoch += 1
                    self.logger.critical('当前训练集已经经过了{0}epoch'.format(self._current_train_epoch))
                    # 关闭之前的file_handle,并重新打开新的handel
                    file_handle.close()
                    file_handle = open(file_handle.name,'rb')
                    continue
                else:
                    break
            batch_size -=1
        return examples,file_handle


    def example_data_cache(self,example_dict={},MaxCaching= 5,CachingDirectory= 'DataCache'):

        """
        对于example进行缓存
        :param example_dict: {'train':example_train,'dev':example_dev,...}
        :param MaxCaching: int 文件夹中的最大缓存数量
        :param CachingDirectory: 缓存的路径
        :return:
        """
        
        # 检查当前的路径情况
        path_cache = os.path.join(self.abs_path,CachingDirectory)
        if not os.path.exists(path_cache):
            # 处理缓存路径不存在的情况
            os.mkdir(path_cache)
        def _check_path_cache():

            """
            检查当前缓存路径是否超过了最大的缓存数量,
            超过了就需要就行删除
            """
            valid_directory = []
            for name in os.listdir(path_cache):
                file_path = os.path.join(path_cache,name)
                if os.path.isdir(file_path) and not name.startswith('.') and not "__pycache__" in name:
                    valid_directory.append({'create_time':os.path.getctime(file_path),
                                                'path':file_path
                                                })
            # 删除之间的缓存路径
            valid_directory.sort(key=lambda x:x['create_time'],reverse = True)
            while len(valid_directory) >=MaxCaching:
                poped_item = valid_directory.pop()
                self.logger.info(f"正在删除缓存文件夹:\n 路径: {poped_item['path']},创建时间:{poped_item['create_time']}")
                shutil.rmtree(['path'])

        # 删除多余的缓存
        _check_path_cache()

        # 创建当前的缓存路径, 文件夹的名称是当前的进程号
        path_cache_current = os.path.join(path_cache,str(os.getpid()))

        for k,v in example_dict.items():
            self.logger.info('正在缓存：{0}'.format(str(k)))
            # 当前example序列化
            self._example_serializer(v,file_name=os.path.join(path_cache_current,str(os.getpid())+ '_'+str(k)+'.record'))










                
                
                
                



















if __name__ == '__main__':
    pass
