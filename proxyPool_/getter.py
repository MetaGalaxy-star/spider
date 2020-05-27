from unit_9.proxyPool_.db import RedisClient
from unit_9.proxyPool_.crawler import Crawler

POOL_UPPRE_THRESHOLD = 10000


class Getter(object):
    def __init__(self):
        self.redis = RedisClient()
        self.crawler = Crawler()

    def is_over_threshold(self):
        """
        判断代理池是否达到的了设置的阈值
        :return: 判断结果
        """
        if self.redis.count() >= POOL_UPPRE_THRESHOLD:
            return True
        else:
            return False

    def run(self):
        print('获取器开始执行')
        if not self.is_over_threshold():
            for callable_label in range(self.crawler.__CrawlFunCount__):
                callback = self.crawler.__CrawlerFunc__[callable_label]
                proxies = self.crawler.get_proxy(callback)
                for proxy in proxies:
                    self.redis.add(proxy)
