import json
import csv
import requests
import os

page = 3

cookies = "Your cookie"
base_url = 'https://api.bilibili.com/x/v2/history?pn={}&jsonp=jsonp'


def setUp_header(cookies):
    """
    存在反爬机制，设置请求头
    :param cookies: 你的账号下的cookie
    :return: 请求头
    """
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Cookie': cookies,
        'Host': 'api.bilibili.com',
        'Referer': 'https://www.bilibili.com/account/history',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/83.0.4103.116 Safari/537.36'
    }
    return headers


def everyOne_requests(url, headers):
    """
    每条链接都爬取一遍
    :param url: 爬取链接
    :param headers: 请求头
    :return: 抓取到的文本数据
    """
    response = requests.get(url, headers=headers).content.decode('utf-8')
    return json.loads(response)


def get_info(jsonData):
    """
    提取json数据下我们需要数据
    :param jsonData: 爬取到的数据
    :return: 我们需要的字典列表信息
    """
    info = []
    for data in jsonData['data']:
        # print(data['aid'], '\t\t', data['cid'], '\t\t', data['owner']['name'], '\t\t', data['tname'], '\t\t',
        #       data['title'], '\t\t', data['stat']['danmaku'], '\t\t', data['stat']['reply'], '\t\t',
        #       data['stat']['favorite'], '\t\t', data['stat']['coin'], '\t\t', data['stat']['share'], '\t\t',
        #       data['stat']['like'])  # '\t\t',data['desc']
        dict = {
            'aid': data['aid'],
            'cid': data['cid'],
            'name': data['owner']['name'],
            'tname': data['tname'],
            'title': data['title'],
            'view': data['stat']['view'],
            'danmaku': data['stat']['danmaku'],
            'reply': data['stat']['reply'],
            'favorite': data['stat']['favorite'],
            'coin': data['stat']['coin'],
            'share': data['stat']['share'],
            'like': data['stat']['share']
        }
        info.append(dict)
    return info


def save_csv(dictList):
    """
    把数据保存到csv文件里
    :param dictList:
    :return:
    """
    fieldnames = ['aid', 'cid', 'name', 'tname', 'title', 'view', 'danmaku', 'reply', 'favorite', 'coin',
                  'share', 'like']
    if os.path.exists('F:/jupyter/exam/data2.csv'):
        with open('F:/jupyter/exam/data2.csv', 'a', encoding="gb18030", newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            for info in dictList:
                writer.writerow(info)
    else:
        with open('F:/jupyter/exam/data2.csv', 'w', encoding="gb18030", newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for info in dictList:
                writer.writerow(info)


if __name__ == '__main__':
    dictlists = []
    headers = setUp_header(cookies)
    for page in range(1, 4):
        url = base_url.format(page)
        jsonData = everyOne_requests(url, headers=headers)
        dictlists.append(get_info(jsonData))
    for dictlist in dictlists:
        save_csv(dictlist)
