#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : {{create_time}}
# @Author : by {{author_name}}
# @File : train.py
# @Email : {{email}}
import math
import time
class BatchGenerator():

    def __init__(self,data_list,batch_size = 9):
        self._data = data_list

        self._max_batch = math.ceil(len(data_list)/batch_size)
        self._current_batch = 0
        self._batch_size = batch_size

    def __len__(self):

        return len(self._data)

    def __iter__(self):

        return self
    def __next__(self):
        # print(self._current_batch)

        if self._current_batch == (self._max_batch):
            self._current_batch = 0
            raise StopIteration
        else:

            r = self._data[self._current_batch*self._batch_size:(self._current_batch+1)*self._batch_size]
            self._current_batch += 1
            return r

if __name__ == '__main__':
    import sys
    data  = list(range(50))
    a = BatchGenerator(data)

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

