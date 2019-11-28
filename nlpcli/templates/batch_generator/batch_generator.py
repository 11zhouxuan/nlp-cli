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

def shuffle_aligned_list(data):

    random.shuffle(data)

class BatchGenerator():

    def __init__(self,data_list,batch_size = 16,data_type = 'train',shuffle = True):

        self._data = data_list
        self._max_batch = math.ceil(len(data_list)/batch_size)
        self._current_batch = 0
        self._batch_size = batch_size
        self._data_type = data_type
        self._shuffle = shuffle
        if len(self)<self._batch_size:
            raise ValueError('batch size greater than length of data: {0}>{1}'.format(self._batch_size,len(self)))

    def __len__(self):

        return len(self._data)

    def __iter__(self):

        return self
    def __next__(self):
        # print(self._current_batch)

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
        return r

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

