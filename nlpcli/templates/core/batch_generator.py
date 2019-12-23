#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : {{create_time}}
# @Author : by {{author_name}}
# @File : train.py
# @Email : {{email}}
import math
import time
import numpy as np
import random
from core import DataProcess
DP = DataProcess()
def shuffle_aligned_list(data):
    random.shuffle(data)

class BatchGenerator():

    def __init__(self,data_list,batch_size = 16,data_type = 'train',shuffle = True,fields = []):

        """

        :param data_list: [example1,example2,...]
        :param batch_size: int
        :param data_type: str, train or test
        :param shuffle: bool, if is true, the data will be shuffled after every epoch
        :param fields: return key in example when 'next' is called
        """

        self._data = data_list
        self._max_batch = math.ceil(len(data_list)/batch_size)
        self._current_batch = 0
        self._batch_size = int(batch_size)
        self._data_type = data_type
        self._shuffle = shuffle
        self._fields = fields
        if not self._fields:
            raise ValueError('Fields can not be empty, current fields: {0}'.format(str(self._fields)))
        if len(self)<self._batch_size:
            raise ValueError('batch size greater than length of data: {0}>{1}'.format(self._batch_size,len(self)))
        self._FeaturePaddingStrOrInt = DP.config['TaskInput']['FeaturePaddingStrOrInt']
        if isinstance(self._FeaturePaddingStrOrInt,str):
            self._FeaturePaddingInt = DP._vacob[self._FeaturePaddingStrOrInt]
        elif isinstance(self._FeaturePaddingStrOrInt,int):
            self._FeaturePaddingInt = self._FeaturePaddingStrOrInt
        else:
            raise ValueError('FeaturePaddingStrOrInt in config must be str or int: {0}'.format(str(self._FeaturePaddingStrOrInt)))
    def __len__(self):

        return len(self._data)

    def __iter__(self):

        return self
    def _convert_to_numpy(self,r):

        """
        将next函数中得到的list转化成numpy格式
        :param r:
        :return: dict, key 为self._fields, 值为numpy格式的ids
        """
        res = {}
        for field in self._fields:
            field_ids = [rr[field+'_ids'] for rr in r]
            max_len = self._padding(field_ids)
            res[field + '_max_len'] = max_len
            res[field] = np.array(field_ids)
        return res
    def _padding(self,list_by_list):

        """
        根据 list_by_list 中的最大长度进行padding
        :param list_by_list: list
        :return:
        """
        lens = [len(l) for l in list_by_list]
        max_len = max(lens)
        [l.extend([self._FeaturePaddingInt]*(max_len-len(l))) for l in list_by_list]
        return max_len

    def __next__(self):

        if self._current_batch == (self._max_batch):
            self._current_batch = 0
            if self._data_type != 'train':
                raise StopIteration
            else:
                # 对于train可能需要重新shuffle
                if self._shuffle:
                    shuffle_aligned_list(self._data)
        if self._current_batch==(self._max_batch-1) and self._data_type=='train':
            # 训练过程中的最后一个batch需要进行额外的一个拼接
            r1 = self._data[self._current_batch*self._batch_size:(self._current_batch+1)*self._batch_size]
            r2 = self._data[:(self._batch_size - len(self)+ self._current_batch*self._batch_size)]
            r = r1 + r2

        else:
            r = self._data[self._current_batch*self._batch_size:(self._current_batch+1)*self._batch_size]
        self._current_batch += 1
        # TODO 添加padding策略,并且将数据转化成numpy再输出

        res = self._convert_to_numpy(r)
        return res

if __name__ == '__main__':
    import sys
    data  = list(range(20))
    a = BatchGenerator(data,shuffle=False)

    print(sys.getsizeof(data))
    print(sys.getsizeof(a))
    del data

    while True:
        try:
            print(next(a))
            time.sleep(2)
        except StopIteration:
            break

    while True:
        try:
            print(next(a))
            time.sleep(2)
        except StopIteration:
            break

