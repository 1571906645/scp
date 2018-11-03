import re
import requests
from bs4 import BeautifulSoup
import os
import threading
import time


class Getscp(threading.Thread):
    basepath = 'D:\scp/'
    baseurl = 'http://scp-wiki-cn.wikidot.com/'
    headers = {
        'Connection': 'keep-alive',
        'Host': 'scp-wiki-cn.wikidot.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
    }

    def __init__(self, sstart, end):
        threading.Thread.__init__(self)
        self.sstart = sstart
        self.end = end

    def run(self):
        urllist = self.get_url()
        self.get_message(urllist)

    def get_url(self):
        urllist = []
        for i in range(self.sstart, self.end):
            if i < 100:
                url = self.baseurl + 'scp-' + '0' * (3 - len(str(i))) + str(i)
            else:
                url = self.baseurl + 'scp-' + str(i)
            urllist.append(url)
        return urllist

    def get_message(self, urllist):
        self.get_url()
        for url in urllist:
            name = url.split('/')[-1]
            mes, img = self.get_response(url)
            self.save_scp(mes=mes, img=img, name=name)

    def get_response(self, url):
        print(url)
        response = requests.get(url, headers=self.headers)
        bs = BeautifulSoup(response.text, 'lxml')
        page = bs.find(id='page-content')
        mes = page.text
        try:
            img = page.find('img').attrs['src']
        except AttributeError:
            img = None
            print('没有图片')
        return mes, img

    def save_scp(self, mes, img, name):
        path = self.basepath + name + '/'
        if not os.path.exists(path):
            os.makedirs('D:\scp/' + name)
        with open(path + name + '.txt', 'w', encoding='utf-8') as f:
            f.write(mes)
            f.close()
        if img:
            response = requests.get(img)
            with open(path + name + '.jpg', 'wb') as f:
                f.write(response.content)
                f.close()


time1 = time.time()
# Getscp(1004, 1104).run()
for s in range(1204, 1404, 10):
    t = Getscp(s, s + 10)
    t.start()
time2 = time.time()
print(time2 - time1)
