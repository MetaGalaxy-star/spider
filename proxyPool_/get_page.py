import requests
from pyquery import PyQuery as pq
from fake_useragent import UserAgent

userAgent = UserAgent()
headers = {
    'user-agent':userAgent.chrome
}
response_state =[200]
def get_page(url):
    try :
        response = requests.get(url,headers=headers,timeout=15)
        if response.status_code in response_state :
            return response.content.decode('utf-8')
        else:
            return False
    except Exception:
        return False
"""
以下是页面抓取测试，可忽略
"""
def xici():
    text = get_page('https://www.xicidaili.com/nn/')
    doc2 = pq(text)
    list01 = doc2('tr .country:first-child').siblings('td:nth-child(2)').text().split(' ')
    list02 = doc2('tr .country:first-child').siblings('td:nth-child(3)').text().split(' ')
    for i in range(0, len(list01)):
        print(list01[i] + ':' + list02[i])

def worldIp(pages):
    for page in range(1,pages+1):
        text = get_page('https://ip.jiangxianli.com/?page='+str(page))
        doc = pq(text)
        doc1 = pq(doc('tbody td'))
        list00 = doc1('td:first-child').text().split(' ')
        list01 = doc1('td:nth-child(2)').text().split(' ')
        for i in range(0, len(list00)):
            print(list00[i] + ':' + list01[i])

def proxyList():
    text = get_page('https://list.proxylistplus.com/Fresh-HTTP-Proxy-List-1')
    doc = pq(text)
    list01 = doc('table.bg .cells').children('td:nth-child(2)').text().split(' ')
    list02 = doc('table.bg .cells').children('td:nth_child(3)').text().split(' ')
    for i in range(0, len(list01)):
        print(list01[i] + ':' + list02[i])

if __name__ == '__main__':
    worldIp(3)