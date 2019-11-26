#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : {{create_time}}
# @Author : by {{author_name}}
# @File : {{file_name}}
# @Email : {{email}}
import os
import yaml
# from log.log import logger
#from auto_device import get_max_remain_gpu
from input_mod.txt2example import LoadTxt
from globalcontrol.dataprocessing import DataProcess
from input_mod.tokennization import Tokenizer
DP = DataProcess()
def main(**kwargs):
    with open('/config_test.yml') as file_config:
        config = yaml.load(file_config)
    DP.config = config # 将配置文件绑定到DP
    # txt2example
    example_loader = LoadTxt()
    train_examples = example_loader(path_txt = config['path_train'])
    dev_examples = example_loader(path_txt = config['path_dev'])
    test_examples = example_loader(path_txt = config['path_test'])

    # tokenization--分词
    tokenizer = Tokenizer()
    tokenizer(train_examples)
    tokenizer(dev_examples)
    tokenizer(test_examples)

    # 特征提取,token转化成id


if __name__=="__main__":
    main()











if __name__ == '__main__':
    pass
