import asyncio
import time

import aiohttp
from aiohttp import ClientError, ClientConnectorError
from unit_9.proxyPool_.db import RedisClient

VALID_STATUS_CODES = [200]
TEST_URL = 'https://weixin.sogou.com/weixin?type=2&query=Python'
BATCH_TEST_SIZE = 100


class Tester(object):
    def __init__(self):
        self.redis = RedisClient()

    async def test_sing_proxyY(self, proxy):
        """
        测试单个代理
        :param proxy: 代理IP
        :return: None
        """
        conn = aiohttp.TCPConnector(verify_ssl=False)
        async with aiohttp.ClientSession(connector=conn) as session:
            try:
                if isinstance(proxy, bytes):
                    proxy = proxy.decode('utf-8')
                real_proxy = 'http://' + proxy
                print('正在测试代理', proxy)
                async with session.get(TEST_URL, proxy=real_proxy, timeout=15) as response:
                    if response.status in VALID_STATUS_CODES:
                        self.redis.max(proxy)
                        print('代理可用', proxy)
                    else:
                        self.redis.decrease(proxy)
                        print('请求响应码不合法', proxy)
            except (ClientError, ClientConnectorError, TimeoutError, ArithmeticError):
                self.redis.decrease([proxy])
                print('代理请求失败~', proxy)
    def run(self):
        """
        测试主函数
        :return: None
        """
        print('测试器开始运行')
        try:
            proxies = self.redis.all()
            loop = asyncio.get_event_loop()
            #批量测试
            for i in range(0,len(proxies),BATCH_TEST_SIZE):
                test_proxies = proxies[i:i+BATCH_TEST_SIZE]
                task = [self.test_sing_proxyY(proxy) for proxy in test_proxies]
                loop.run_until_complete(asyncio.wait(task))
                time.sleep(5)
        except Exception as e :
            print('测试器发生错误',e.args)