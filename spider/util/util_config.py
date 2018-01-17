# coding: utf-8

import random
from enum import Enum

__all__ = [
    "Pattern",
    "NEWS_URL",
    "contain_word",
    "CONFIG_FETCH_MESSAGE",
    "requests_headers",
    "UrlStopWord",
    # "NEW_FLAG"
]

CONFIG_FETCH_MESSAGE = "priority=%s, repeat=%s, url=%s"

# begin url
NEWS_URL = [
    'http://news.ifeng.com',
    'http://news.ifeng.com/listpage/11574/0/1/rtlist.shtml',  # 国际即时新闻
    'http://news.ifeng.com/listpage/11528/0/1/rtlist.shtml',  # 大陆即时新闻
    'http://news.ifeng.com/listpage/11502/0/1/rtlist.shtml',  # 所有即时新闻
    'http://news.ifeng.com/listpage/11490/0/1/rtlist.shtml',  # 台湾即时新闻
    'http://news.163.com'
    #    'http://news.qq.com/'
    # "http://star.finance.ifeng.com/org/200000918"
]

url_dict = {}
save_list = "last_news"


def requests_headers():
    head_connection = ['Keep-Alive', 'close']
    head_accept = ['text/html,application/xhtml+xml,*/*']
    head_accept_language = ['zh-CN,fr-FR;q=0.5', 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3']
    head_user_agent = ['Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
                       'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.95 Safari/537.36',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; rv:11.0) like Gecko)',
                       'Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1',
                       'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070309 Firefox/2.0.0.3',
                       'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070803 Firefox/1.5.0.12',
                       'Opera/9.27 (Windows NT 5.2; U; zh-cn)',
                       'Mozilla/5.0 (Macintosh; PPC Mac OS X; U; en) Opera 8.0',
                       'Opera/8.0 (Macintosh; PPC Mac OS X; U; en)',
                       'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.12) Gecko/20080219 Firefox/2.0.0.12 Navigator/9.0.0.6',
                       'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Win64; x64; Trident/4.0)',
                       'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)',
                       'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C; .NET4.0E)',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Maxthon/4.0.6.2000 Chrome/26.0.1410.43 Safari/537.1 ',
                       'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C; .NET4.0E; QQBrowser/7.3.9825.400)',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0 ',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.92 Safari/537.1 LBBROWSER',
                       'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; BIDUBrowser 2.x)',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/3.0 Safari/536.11']

    # header 为随机产生一套由上边信息的header文件
    header = {
        'Connection': head_connection[random.randrange(0, len(head_connection))],
        'Accept': head_accept[0],
        'Accept-Language': head_accept_language[random.randrange(0, len(head_accept_language))],
        'User-Agent': head_user_agent[random.randrange(0, len(head_user_agent))],
    }
    return header  # 返回值为 header这个字典


# pattern class
class Pattern(object):
    # http://www.ifeng.com/ 停止抓取的关键词
    IFENG_NEWS_PATTERN = '^http://.+\.ifeng\.com\/a\/[0-9]{8}\/[0-9]{5,8}\_0\.shtml$'

    IFENG_NEWS_DETAIL_PATTERN = '^http://.+\.ifeng\.com\/a\/(2017[12]{2}|2018[0-2]{2})[0-9]{2}\/[0-9]{5,8}\_0\.shtml$'
    IFENG_NEWS_RELAYPATTERN = '^http://.+\.ifeng\.com\/[a-z0-9_\/\.]*$'
    # IFENG_NEWS_RELAYPATTERN = '^http://.+\.ifeng\.com/?(.*?)$'

    NETEASE_NEWS_PATTERN = "^http://.+\.163\.com/[178]{2}/[012]{2}\d{2}/\d{2}/.*?.html$"
    NETEASE_RELAY_PATTERN = "^http://.*?\.163\.com/?[a-zA-Z]{0,}/?$"


#
# class NEW_FLAG(Enum):
#     IFENG = "ifeng"
#     NETEASE = '163'
#     QQ = "qq"


class UrlStopWord():
    IFENG_URL_STOP_WORD = ["video",
                           "junjichu",
                           "app", "2009", "2008", "2007", "2006", "2005", "2004", "2003", "2002", "2001",
                           "job", "play", "2013", "2014", "2015", "2016", "2010", "2011", "2012", "huodong",
                           "special", "insight", "health", "fashion",
                           "3g", "3c",
                           "corp", "vip", "star.finance", "hn", "res",
                           "career", "book",
                           "career", "book",
                           "blog", "snapshots", "gentie", "cosmetics", "homedetail", "house",
                           "diantai",
                           "help",
                           "ir", "bbs", "talk", "media", "ient", "isport", "ivc", "inews", "ifinance", "itech",
                           "auto", "ihistory", "try", "wemedia", "comment", "sports",
                           "jiu", "yc", "dm", "null", "quiz", "astro", "finance.ifeng.com",
                           "id", "brand", "baby",
                           "login", "search", "games",
                           "about",
                           "big5",
                           "dol", "tv", "imall", "lehuo", "zhibo", "tuan", "biz"
                           ]


def contain_word(text, words):
    for word in words:
        # 是否含有过滤词汇
        if word in text:
            return True
    return False
