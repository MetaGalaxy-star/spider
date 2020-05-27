import time
from multiprocessing import Process
from unit_9.proxyPool_.api import app
from unit_9.proxyPool_.getter import Getter
from unit_9.proxyPool_.tester import Tester

TESTER_CYCLE = 20
GETTER_CYCLE = 20
TESTER_ENABLE = True
GETTER_ENABLE = True
API_ENABLE = True


class Scheduler():
    def schedule_tester(self, cycle=TESTER_CYCLE):
        """
        定时测试代理
        :param cycle:周期时间
        :return: None
        """
        tester = Tester()
        while True:
            print('测试器开始运行')
            tester.run()
            time.sleep(cycle)

    def schedule_getter(self, cycle=GETTER_CYCLE):
        """
        定时获取代理
        :param cycle: 周期时间
        :return: None
        """
        getter = Getter()
        while True:
            print('开始抓取代理')
            getter.run()
            time.sleep(cycle)

    def schedule_qpi(self):
        """
        开启API
        :return:None
        """
        # app.run(API_HOST,API_PORT)
        app.run()

    def run(self):
        """
        执行入口
        :return: None
        """
        print('代理池开始运行')
        if TESTER_ENABLE:
            tester_process = Process(target=self.schedule_tester)
            tester_process.start()
        if GETTER_ENABLE:
            getter_process = Process(target=self.schedule_getter)
            getter_process.start()
        if API_ENABLE:
            api_process = Process(target=self.schedule_qpi)
            api_process.start()


if __name__ == '__main__':
    # app.debug = True
    Scheduler().run()
