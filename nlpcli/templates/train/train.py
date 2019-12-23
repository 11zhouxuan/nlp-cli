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
DP = DataProcess()
DP.logger = logger
def main(**kwargs):
    with open('/config.yml') as file_config:
        config = yaml.load(file_config)
    DP.config = config # 将配置文件绑定到DP
    DP.get_feature_vocab() # 从配置文件中获取字符对应的 vocabulary
    DP.get_label_map() # 从配置文件中获取label map
    # txt2example
    example_loader = LoadTxt()
    train_examples = example_loader(path_txt = config['path_train'])
    dev_examples = example_loader(path_txt = config['path_dev'])
    test_examples = example_loader(path_txt = config['path_test'])

    # tokenization--分词, token_fields关键字需要手动填充
    tokenizer = Tokenizer()
    tokenizer(train_examples,token_fields = [],expand_fn = {})
    tokenizer(dev_examples,token_fields = [],expand_fn = {})
    tokenizer(test_examples,token_fields = [],expand_fn = {})

    # 特征提取,token转化成id
    DP.token_to_id(DP._vocab,fields = [],example_lists = [train_examples,dev_examples,test_examples]) # fields 一般是以_tokenized 后缀的字段
    DP.token_to_id(DP._label_map,fields = [], example_lists = [train_examples,dev_examples,test_examples])

    # 分别将example_list送入到生成器中

    train_data = BatchGenerator(train_examples,
                   batch_size = config['TrainParamaters']['BatchSize'],
                   data_type = 'train',
                   shuffle = True,
                   fields = [])
    dev_data = BatchGenerator(dev_examples,
                   batch_size = config['EvaluateParameters'],
                   data_type = 'test',
                   shuffle = False,
                   fields = [])
    test_data = BatchGenerator(test_examples,
                   batch_size = config['EvaluateParameters'],
                   data_type = 'test',
                   shuffle = False,
                   fields = [])













if __name__=="__main__":
    main()

