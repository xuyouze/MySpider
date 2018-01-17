# coding: utf-8


import random
from queue import Queue
import requests
import time
from bs4 import BeautifulSoup
from multiprocessing import Process
from ..util.util_config import requests_headers
from ..util.util_fetch import get_error_info


class Proxies(object):
    """docstring for Proxies"""

    def __init__(self, page=5):
        self.proxies = []
        self.verify_pro = []
        self.page = page
        self.headers = requests_headers()

    def get_proxies(self):
        page = random.randint(1, 10)
        page_stop = page + self.page
        while page < page_stop:
            url = 'http://www.xicidaili.com/nt/%d' % page
            html = requests.get(url, headers=self.headers).content
            soup = BeautifulSoup(html, 'lxml')
            ip_list = soup.find(id='ip_list')
            for odd in ip_list.find_all(class_='odd'):
                protocol = odd.find_all('td')[5].get_text().lower() + '://'
                self.proxies.append(protocol + ':'.join([x.get_text() for x in odd.find_all('td')[1:3]]))
            page += 1

    def working(self) -> list:
        print("%s start " % (self.__class__.__name__))
        try:
            self.get_proxies()
            self.get_proxies_nn()
            self.verify_proxies()

        except Exception:
            print("%s error: %s" % (self.__class__.__name__, get_error_info()))
        return self.proxies

    def get_proxies_nn(self):
        page = random.randint(1, 10)
        page_stop = page + self.page
        while page < page_stop:
            url = 'http://www.xicidaili.com/nn/%d' % page
            html = requests.get(url, headers=self.headers).content
            soup = BeautifulSoup(html, 'lxml')
            ip_list = soup.find(id='ip_list')
            for odd in ip_list.find_all(class_='odd'):
                protocol = odd.find_all('td')[5].get_text().lower() + '://'
                self.proxies.append(protocol + ':'.join([x.get_text() for x in odd.find_all('td')[1:3]]))
            page += 1

    def verify_proxies(self):

        # 验证后的代理
        queue = Queue()
        print('verify proxy........')

        for proxy in self.proxies:
            protocol = 'https' if 'https' in proxy else 'http'
            proxies = {protocol: proxy}
            try:
                if requests.get('http://www.baidu.com', proxies=proxies, timeout=2).status_code == 200:
                    print('success %s' % proxy)
                    queue.put(proxy)
            except:
                print('fail %s' % proxy)

        self.proxies = []
        while 1:
            try:
                self.proxies.append(queue.get(timeout=1))
            except:
                break
        print('verify_proxies done!')

    def verify_one_proxy(self, old_queue, new_queue):
        while 1:
            proxy = old_queue.get()
            if proxy == 0: break
