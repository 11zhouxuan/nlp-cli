#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : {{create_time}}
# @Author : by {{author_name}}
# @File : {{file_name}}
# @Email : {{email}}
import threading
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



    @staticmethod
    def check_config(config):

        """
        检查config是否
        :param config:
        :return:
        """
        pass



if __name__ == '__main__':
    pass
