# -*- coding: utf-8 -*-
# !/usr/bin/env python

"""
-------------------------------------------------
   File Name：    MongodbClient.py
   Description :  封装mongodb操作
   Author :       A.L.
   date：         2018/8/16
-------------------------------------------------
   Change Activity:
        2018/08/16:    add RedisClusterClient support   A.L.
-------------------------------------------------
"""

from package.utils import EnvUtil
import random
from rediscluster import StrictRedisCluster


class RedisClusterClient(object):
    """
    Reids cluster client
    """

    def __init__(self, name, startup_nodes, password):
        """
        init
        :param name: hashtable name
        :param startup_nodes: cluster nodes
        :param password: passwords
        :return:
        """
        self.name = name
        self.__conn = StrictRedisCluster(startup_nodes=startup_nodes, password=password, socket_timeout=200)

    def get(self, proxy):
        """
        get an item
        从hash中获取对应的proxy, 使用前需要调用changeTable()
        :param proxy:
        :return:
        """
        data = self.__conn.hget(name=self.name, key=proxy)
        if data:
            return data.decode('utf-8') if EnvUtil.PY3 else data
        else:
            return None

    def put(self, proxy, num=1):
        """
        将代理放入hash, 使用changeTable指定hash name
        :param proxy:
        :param num:
        :return:
        """
        data = self.__conn.hset(self.name, proxy, num)
        return data

    def delete(self, key):
        """
        Remove the ``key`` from hash ``name``
        :param key:
        :return:
        """
        self.__conn.hdel(self.name, key)

    def update(self, key, value):
        self.__conn.hincrby(self.name, key, value)

    def pop(self):
        """
        弹出一个代理
        :return: dict {proxy: value}
        """
        proxies = self.__conn.hkeys(self.name)
        if proxies:
            proxy = random.choice(proxies)
            value = self.__conn.hget(self.name, proxy)
            self.delete(proxy)
            return {'proxy': proxy.decode('utf-8') if EnvUtil.PY3 else proxy,
                    'value': value.decode('utf-8') if EnvUtil.PY3 and value else value}
        return None

    def exists(self, key):
        return self.__conn.hexists(self.name, key)

    def getAll(self):
        item_dict = self.__conn.hgetall(self.name)
        if EnvUtil.PY3:
            return {key.decode('utf8'): value.decode('utf8') for key, value in item_dict.items()}
        else:
            return item_dict

    def getNumber(self):
        """
        Return the number of elements in hash ``name``
        :return:
        """
        return self.__conn.hlen(self.name)

    def changeTable(self, name):
        self.name = name


if __name__ == '__main__':
    REDIS_NODES = [
        {'host': '192.168.245.130', 'port': 1079},
        {'host': '192.168.245.130', 'port': 1080},
        {'host': '192.168.245.130', 'port': 1081},
        {'host': '192.168.245.130', 'port': 1082},
        {'host': '192.168.245.130', 'port': 1083},
        {'host': '192.168.245.130', 'port': 1084},
    ]

    REDIS_PASSWORD = 'qizvg5DB'
    redis_con = RedisClusterClient(name='proxy', startup_nodes=REDIS_NODES, password=REDIS_PASSWORD)
    # redis_con.put('abc')
    # redis_con.put('123')
    # redis_con.put('123.115.235.221:8800')
    # redis_con.put(['123', '115', '235.221:8800'])
    # print(redis_con.getAll())
    # redis_con.delete('abc')
    # print(redis_con.getAll())

    # print(redis_con.getAll())
    redis_con.changeTable('raw_proxy')
    redis_con.pop()

    # redis_con.put('132.112.43.221:8888')
    # redis_con.changeTable('proxy')
    print(redis_con.get_status())
    print(redis_con.getAll())
