# coding: utf-8

from ..util import *
import time
import requests


class Fetch(object):
    def __init__(self, max_repeat=3, sleep_time=1):
        """
            construction
        :param sleep_time:default 1, sleeping time after a fetching for a url
        """

        self._max_repeat = max_repeat
        self._sleep = sleep_time

    def working(self, priority: int, url: str, repeat: int, url_filter, proxies=None) -> (int, bool, object):
        print("%s start: %s" % (self.__class__.__name__, CONFIG_FETCH_MESSAGE % (priority, repeat, url)))
        try:
            fetch_result, proxies_state, content = self.url_fetch(priority, url, repeat, url_filter, proxies)

        except requests.RequestException:
            if repeat >= self._max_repeat:
                fetch_result, proxies_state, content = -1, False, None
                print("%s error: %s, %s" % (self.__class__.__name__, get_error_info(),
                                            CONFIG_FETCH_MESSAGE % (priority, repeat, url)))
            else:
                fetch_result, proxies_state, content = 0, True, None
                print("%s repeat: %s, %s" % (self.__class__.__name__, get_error_info(),
                                             CONFIG_FETCH_MESSAGE % (priority, repeat, url)))
                return fetch_result, proxies_state, content
        except Exception:
            fetch_result, proxies_state, content = -1, True, None
            print("%s error: %s, %s" % (self.__class__.__name__, get_error_info(),
                                        CONFIG_FETCH_MESSAGE % (priority, repeat, url)))

        print("%s end: fetch_result = %s, proxies_state=%s, url=%s" % (self.__class__.__name__, fetch_result,
                                                                       proxies_state, url))
        return fetch_result, proxies_state, content

    def url_fetch(self, priority: int, url: str, repeat: int, url_filter: UrlFilter, proxies=None) -> (
            int, bool, object):
        """
            main fetch  use util.fetch to parse
        :param priority:
        :param url: fetch url
        :param repeat:
        :param url_filter: filter the content from fetch
        :param proxies:
        :return: fetch result, proxies_state ,content of fetch
        """

        flag = url_filter.check_news(url)
        if flag == 0:
            return -1, True, None

        response = requests.get(url=url, proxies=proxies, headers=requests_headers(), timeout=5)
        # get content
        # if response.status_code == requests.codes.ok:
        content = response.text.encode(response.encoding).decode('utf-8') if response.encoding == 'ISO-8859-1' else response.text

        # flag == 1 means the url is news

        url_filter.update(url, 0)
        if flag == 1:
            return 1, True, content
        # flag == 2 means the url is relay can continue fetch
        elif flag == 2:
            # return list
            return 2, True, url_filter.parse_relay_content(content)
