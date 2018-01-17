# coding: utf-8
import time

from .thread_base import BaseThread
from .thread_config import FlagEum


class FetchThread(BaseThread):
    def __init__(self, name, worker, pool):
        BaseThread.__init__(self, name, worker, pool)
        self._proxies = None

    def working(self):
        if self._pool.get_proxies_flag() and (not self._proxies):
            self._proxies = self._pool.get_a_task(FlagEum.PROXIES)

        priority, counter, url, repeat = self._pool.get_a_task(FlagEum.URL_FETCH)

        fetch_result, proxies_state, content = self._worker.working(priority, url, repeat, self._pool._url_filter,
                                                                    self._proxies)

        # the url is news
        if fetch_result == 1:
            self._pool.update_number_dict(FlagEum.URL_FETCH_SUCC, +1)
            self._pool.add_a_task(FlagEum.HTML_PARSE, (priority, counter, url, content))
        # the url is relay cite
        elif fetch_result == 2:
            for n in content:
                if self._pool._url_filter.check_news(n) == 1:
                    self._pool.add_a_task(FlagEum.URL_FETCH, (priority + 1, counter, n, 0))
                else:
                    self._pool.add_a_task(FlagEum.URL_FETCH, (priority, counter, n, 0))
        elif fetch_result == 0:
            self._pool.add_a_task(FlagEum.URL_FETCH, (priority + 1, counter, url, repeat + 1))
        else:
            self._pool.update_number_dict(FlagEum.URL_FETCH_FAIL, +1)

        if (not proxies_state) and self._proxies:
            self._pool.update_number_dict(FlagEum.PROXIES_FAIL, +1)
            self._pool.finish_a_task(FlagEum.PROXIES)
            self._proxies = None

        self._pool.finish_a_task(FlagEum.URL_FETCH)

        while (self._pool.get_number_dict(FlagEum.HTML_PARSE_NOT) > 500) or (
                    self._pool.get_number_dict(FlagEum.ITEM_SAVE_NOT) > 500):
            print("%s[%s] sleep 5 seconds because of too many 'HTMl_PARSE_NOT' or 'ITEM_SAVE_NOT'..." % (
                self.__class__.__name__, self.getName()))
            time.sleep(5)
        return False if fetch_result == -2 else True
