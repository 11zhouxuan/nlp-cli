#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : {{create_time}}
# @Author : by {{author_name}}
# @File : {{file_name}}
# @Email : {{email}}
import os
import yaml
from log import logger
#from auto_device import get_max_remain_gpu
from input_mod import LoadTxt,Tokenizer
from core import DataProcess,BatchGenerator
from model import Model
import json
DP = DataProcess()
abs_path = os.path.dirname(__file__)
DP.abs_path = abs_path # 项目的主路径
DP.logger = logger

def _txt2id(**kwargs):

    """
    将txt转化为id, 这一步可进行cache
    """
    config = DP.config
    # txt2example
    example_loader = LoadTxt()
    train_examples = example_loader(path_txt = config['PathTrain'])
    dev_examples = example_loader(path_txt = config['PathDev'])
    test_examples = example_loader(path_txt = config['PathTest'])

    # tokenization--分词, token_fields关键字需要手动填充
    tokenizer = Tokenizer()
    tokenizer(train_examples,token_fields = [],expand_fn = {})
    tokenizer(dev_examples,token_fields = [],expand_fn = {})
    tokenizer(test_examples,token_fields = [],expand_fn = {})

    # 特征提取,token转化成id
    DP.token_to_id(DP._vocab,fields = [],example_lists = [train_examples,dev_examples,test_examples]) # fields 一般是以_tokenized 后缀的字段
    DP.token_to_id(DP._label_map,fields = [], example_lists = [train_examples,dev_examples,test_examples])

    # 进行缓存
    if config['DataCache']['CachingCurrentData']:
        DP.example_data_cache(example_dict={
            'train':train_examples,
            'dev':dev_examples,
            'test':test_examples
        },
        MaxCaching = config['DataCache']['MaxCaching'],
        CachingDirectory = config['DataCache']['CachingDirectory']
        )
    return train_examples,dev_examples,test_examples
def _BatchGenerator(train_examples = '',dev_examples= '',test_examples = ''):

    """
    将数据变成生成器
    :param train_examples:  str or list, 训练样本的路径
    :param dev_examples: str or list,
    :param test_examples:
    :return:
    """
    config = DP.config

    # 分别将example_list送入到生成器中
    data_train = BatchGenerator(train_examples,
                   batch_size = config['TrainParamaters']['BatchSize'],
                   data_type = 'train',
                   shuffle = True,
                   fields = [])
    data_dev = BatchGenerator(dev_examples,
                   batch_size = config['EvaluateParameters'],
                   data_type = 'test',
                   shuffle = False,
                   fields = [])
    data_test = BatchGenerator(test_examples,
                   batch_size = config['EvaluateParameters'],
                   data_type = 'test',
                   shuffle = False,
                   fields = [])
    return data_train,data_dev,data_test

def _printconfig():

    # 打印当前参数
    js = json.dumps(DP.config, indent= 4,separators=(',',':'))
    logger.info('当前的配置参数为:\n {0}'.format(js))


def main(**kwargs):
    # 读取配置文件
    with open('/config.yml') as file_config:
        config = yaml.load(file_config)
    DP.config = config # 将配置文件绑定到DP
    DP.get_feature_vocab() # 从配置文件中获取字符对应的 vocabulary
    DP.get_label_map() # 从配置文件中获取label map

    # 如果使用缓存就不需要进行text文本的解析
    if config['DataCache']['UseCachedData']:
        train_examples = config['DataCache']['CachedPathTrain']
        dev_examples = config['DataCache']['CachedPathDev']
        test_examples = config['DataCache']['CachedPathTest']
    else:
        train_examples,dev_examples,test_examples = _txt2id()

    # 分别将example_list送入到生成器中
    data_train,data_dev,data_test =  _BatchGenerator(train_examples=train_examples,
                    dev_examples=dev_examples,
                    test_examples=test_examples)


    model = Model()

    # 训练之前打印一下参数
    _printconfig()

    # 模型进行fit
    model.fit(
        data_train  = data_train,
        data_dev = data_dev,
        data_test = data_test
    )

if __name__=="__main__":
    main()

