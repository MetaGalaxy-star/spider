MAX_SCORE = 100
MIN_SCORE = 0
INITIAL_SCORE = 10
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_PASSWORD = None
REDIS_KEY = 'proxies'

import redis
from random import choice
from unit_9.proxyPool_.empty import PoolEmptyException


class RedisClient(object):
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD):
        """
        初始化
        :param host: redis地址
        :param port: redis 端口
        :param password: redis密码
        """
        self.db = redis.StrictRedis(host=host, port=port, password=password, decode_responses=True)
        print(host, port, password)

    def add(self, proxy, score=INITIAL_SCORE):
        """
        添加代理，设置分数为最高
        :param proxy: 代理IP
        :param score: 初次给定分数
        :return: 添加结果
        """
        # print("正在入库", proxy)
        if not self.db.zscore(REDIS_KEY, proxy):
            return self.db.zadd(REDIS_KEY, {proxy: score})

    def random(self):
        """
        随机获取有效代理，首先尝试获取最高分数的代理，如果最高分数不存在，则按照排名获取，否则异常
        :return: 随机代理
        """
        result = self.db.zrangebyscore(REDIS_KEY, MAX_SCORE, MAX_SCORE)
        print(result)
        if len(result) > 0:
            print("满分IP :")
            return choice(result)
        else:
            result = self.db.zrevrange(REDIS_KEY, 90, 100)
            print("=======")
            print(result)
            if len(result):
                print("不是满分IP :")
                return choice(result)
            else:
                raise PoolEmptyException

    def decrease(self, proxy):
        """
        代理值减一分，分数小于0则删除代理
        :param proxy: 测试不理想的代理IP
        :return:添加处理结果
        """
        score = self.db.zscore(REDIS_KEY, proxy)
        if score and score > MIN_SCORE:
            print('代理', proxy, '当前分数', score, '减1')
            return self.db.zincrby(REDIS_KEY, -1, proxy)
        else:
            print('代理', proxy, '当前分数', score, '移除')
            return self.db.zrem(REDIS_KEY, proxy)

    def exists(self, proxy):
        """
        判断是否存在
        :param proxy: 代理IP
        :return: None
        """
        return not self.db.zscore(REDIS_KEY, proxy) == None

    def max(self, proxy):
        """
        将代理设置为 MAX_SCORE
        :param proxy: 测试通过的代理IP
        :return: 处理结果
        """
        print('代理可用', proxy, '可用，设置为', MAX_SCORE)
        return self.db.zadd(REDIS_KEY, {proxy: MAX_SCORE})   #注意这里的语法，与某些教程不一致。可以看看这块的源码

    def count(self):
        """
        获取数量
        :return: 代理总量
        """
        return self.db.zcard(REDIS_KEY)

    def all(self):
        """
        获取全部代理
        :return: 全部代理
        """
        return self.db.zrangebyscore(REDIS_KEY, MIN_SCORE, MAX_SCORE)