from flask import Flask, g
from unit_9.proxyPool_.db import RedisClient

__all__ = ['app']
app = Flask(__name__)


def get_conn():
    if not hasattr(g, 'redis'):
        g.redis = RedisClient()
    return g.redis

@app.route('/')
def index():
    """
    首页内容
    :return: 首页HTML代码
    """
    return '<h2>WelCome to proxy Pool System</h2>'


@app.route('/random')
def get_proxy():
    """
    随机获取可用代理
    :return:随机代理IP
    """
    conn = get_conn()
    proxy = conn.random()
    return str(proxy)

@app.route('/count')
def get_count():
    """
    获取代理池总量
    :return: 代理IP总数量
    """
    conn = get_conn()
    return str(conn.count())

if __name__ == '__main__':
    """
    测试
    """
    app.debug = True
    app.run()