import requests
from bs4 import BeautifulSoup

url = 'https://comment.bilibili.com/197274464.xml'
headers = {
    'UserAgent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
    # 'cookie':"_uuid=105E875C-3062-A5CC-D3FE-5BC9BA48023715052infoc; buvid3=D43CFE45-7BAC-43C2-8651-C937A6C02D73155829infoc; LIVE_BUVID=AUTO6415696588155254; sid=d2fj5s2s; CURRENT_FNVAL=16; stardustvideo=1; rpdid=|(J|~u)k)J|R0J'ulYmYlm~Y); im_notify_type_472723842=0; laboratory=1-1; DedeUserID=472723842; DedeUserID__ckMd5=4faa3ca1ebf998ca; SESSDATA=45d6be1d%2C1599627808%2C35aa5*31; bili_jct=44ca56123999bd9fb81c33f8f0e86fae; CURRENT_QUALITY=32; PVID=1; bfe_id=018fcd81e698bbc7e0648e86bdc49e09; bp_video_offset_472723842=407553827588728391; bp_t_offset_472723842=407553827588728391"
}
text = requests.get(url=url,headers=headers).content.decode('utf-8')
soup = BeautifulSoup(text,'lxml')
with open('barrage.txt','w') as file:
    for d in soup.i.select('d'):
        file.write(d.string)