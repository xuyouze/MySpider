# coding: utf-8
from bs4 import BeautifulSoup

from ..util import *
from .news import News
import re


class Parse(object):
    def __init__(self):
        pass

    def working(self, priority: int, url: str, content: object) -> (bool, News):
        print("%s start: %s" % (self.__class__.__name__, url))
        news = None
        flag = False
        try:
            flag, news = self.htm_parse(priority, url, content)
        except Exception:
            print("%s error: %s, %s" % (
                self.__class__.__name__, get_error_info(), url))

        print("%s end: parse_result=%s, url=%s" % (self.__class__.__name__, flag, url))
        return flag, news

    def htm_parse(self, priority: int, url: str, content: object) -> (bool, News):

        """
        parse the content of a url, you can rewrite this function, parameters and return refer to self.working()
        """
        soup = BeautifulSoup(content, 'lxml')

        date, source, title, content = parse_content(url, soup)

        date = re.sub("[^\d]", "", date)
        date += "00" if len(date) < 14 and date else ""
        date = "%s-%s-%s %s:%s:%s" % (date[:4], date[4:6], date[6:8], date[8:10], date[10:12], date[12:14])
        # 过滤 不规范的新闻
        if "404" in title or len(date) != 19:
            print("error: title:%s date: %s" % (title, date))
            return 0, None
        content = title if not content else re.sub("\n+", "", content)
        print(url, content)
        news = News(source=source, title=title, time=date, url=url, content=content)
        return 1, news
