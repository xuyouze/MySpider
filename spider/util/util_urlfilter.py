# coding: utf-8
import threading

from bs4 import BeautifulSoup

from .util_config import *
import re



class UrlFilter(object):
    def __init__(self, url_dict):
        self._filter = Pattern
        self._url_dict = url_dict
        self.lock = threading.Lock()

    def check_news(self, url) -> int:

        if re.search(self._filter.IFENG_NEWS_DETAIL_PATTERN, url) or re.search(self._filter.NETEASE_NEWS_PATTERN, url):
            return 1
        if re.search(self._filter.IFENG_NEWS_PATTERN, url):
            return 0
        else:
            return 2

    def update(self, url, value):
        self.lock.acquire()
        self._url_dict[url] = value
        self.lock.release()

    def parse_relay_content(self, content: str) -> list:
        urls = set()
        soup = BeautifulSoup(content, 'lxml')

        links = soup.findAll(name='a', href=re.compile(Pattern.IFENG_NEWS_RELAYPATTERN))
        if links:
            for link in links:
                url = link.get("href")
                if self.check_news(url) and not contain_word(url,
                                                             UrlStopWord.IFENG_URL_STOP_WORD) and self._url_dict.get(
                    url, 1):
                    urls.add(url)
                    self.update(url, 1)
        else:

            news_links = soup.findAll(name='a', href=re.compile(Pattern.NETEASE_NEWS_PATTERN))

            for link in news_links:
                url = link.get("href")
                if self.check_news(url) and not contain_word(url,
                                                             UrlStopWord.IFENG_URL_STOP_WORD) and self._url_dict.get(
                    url, 1):
                    urls.add(url)
                    self.update(url, 1)
            news_links = soup.findAll(name='a', href=re.compile(Pattern.NETEASE_RELAY_PATTERN))

            for link in news_links:
                url = link.get("href")
                if self.check_news(url) and not contain_word(url,
                                                             UrlStopWord.IFENG_URL_STOP_WORD) and self._url_dict.get(
                    url, 1):
                    urls.add(url)
                    self.update(url, 1)
        return urls
