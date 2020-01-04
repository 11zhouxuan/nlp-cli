#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : {{create_time}}
# @Author : by {{author_name}}
# @File : {{file_name}}
# @Email : {{email}}
import math
import time
import numpy as np
import random
from core import DataProcess
import os

DP = DataProcess()
def shuffle_aligned_list(data):
    random.shuffle(data)
def parse_config_CachedDataThresholdSize():

    """
    解析config中的 CachedDataThresholdSize参数
    :return:
    """
    units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
    CachedDataThresholdSize = str(DP.config['DataCache']['CachedDataThresholdSize'])
    unit = ''
    digit = ''
    for s in CachedDataThresholdSize:
        if s:
            if s.isdigit() or s=='.':
                digit += s
            else:
                unit +=s
    if unit not in units:
        raise ValueError('unit is not in {0}, but current unit is {1}'.format(str(units),unit))

    number = float(digit)

    unit_index = units.index(unit)
    size_by_B = number*(1024**unit_index)
    DP.CachedDataThresholdSize = size_by_B



class BatchGenerator():

    def __init__(self,data_list,batch_size = 16,data_type = 'train',shuffle = True,fields = []):

        """

        :param data_list: [example1,example2,...] or str(path)
        :param batch_size: int
        :param data_type: str, train or test
        :param shuffle: bool, if is true, the data will be shuffled after every epoch
        :param fields: return key in example when 'next' is called
        """
        if isinstance(data_list,str):
            # 当前的数据穿进来的是字符串
            if not os.path.exists(data_list):
                raise ValueError('current data path is not valid')
            # 判断文件的大小，文件不大的时候直接读取进来
            file_size = os.path.getsize(data_list)
            # 和config文件中的阈值size进行判断,没有超过就直接全部序列化
            if not hasattr(DP,'CachedDataThresholdSize'):
                parse_config_CachedDataThresholdSize()
            # 从文件中读取数据
            self._data = open(data_list,'rb')
            if file_size > DP.CachedDataThresholdSize:
                self._read_data_from_file = True
                self._file_handel = self._data
            else:
                # 此时直接进行反序列
                self._data = DP._example_inverse_serializer(self._data)
                self._read_data_from_file = False
        else:
            self._data = data_list
            self._max_batch = math.ceil(len(data_list)/batch_size)
            self._read_data_from_file = False
        self._current_batch = 0
        self._batch_size = int(batch_size)
        self._data_type = data_type
        if self._read_data_from_file:
            self._shuffle = False #
            DP.logger.info('注意当前数据利用了缓存,不能整个进行随机打乱')
        self._fields = fields

        # 检查传入字段
        if not self._fields:
            raise ValueError('Fields can not be empty, current fields: {0}'.format(str(self._fields)))
        if not self._read_data_from_file:
            if len(self)<self._batch_size:
                raise ValueError('batch size greater than length of data: {0}>{1}'.format(self._batch_size,len(self)))
        self._FeaturePaddingStrOrInt = DP.config['TaskInput']['FeaturePaddingStrOrInt']
        if isinstance(self._FeaturePaddingStrOrInt,str):
            self._FeaturePaddingInt = DP._vacob[self._FeaturePaddingStrOrInt]
        elif isinstance(self._FeaturePaddingStrOrInt,int):
            self._FeaturePaddingInt = self._FeaturePaddingStrOrInt
        else:
            raise ValueError('FeaturePaddingStrOrInt in config must be str or int: {0}'.format(str(self._FeaturePaddingStrOrInt)))

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
            # TODO 这里如果当前batch太长可能还是需要进行一个
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

        if not self._read_data_from_file:
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
        else:
            r,self._file_handel = DP._example_inverse_serializer_by_batch(
                self._file_handel,
                batch_size = self._batch_size,
                is_train = True if self._data_type=='train' else False
            )
        # example 到padding之后的数组
        # 这里r中的元素可能是list嵌套类型的,特别是当用缓存的时候,一行可能对应多个example
        if isinstance(r[0],list):
            r = sum(r,[])
        # 提取需要的字段,并进行padding
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

