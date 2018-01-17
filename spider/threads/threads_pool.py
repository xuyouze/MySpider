# coding: utf-8
import copy
import queue
import threading

import redis

from ..util import CONFIG_FETCH_MESSAGE
from .threads_inst import *


class ThreadPool(object):
    def __init__(self, fetcher, parser=None, saver=None, proxieser=None, url_filter=None, monitor_sleep_time=5):

        self._inst_fetcher = fetcher  # fetcher instance, subclass of Fetcher
        self._inst_parser = parser  # parser instance, subclass of Parser
        self._inst_saver = saver  # saver instance, subclass of Saver
        self._url_filter = url_filter  # default: None, also can be UrlFilter()

        self._proxieser = proxieser
        self._lock = threading.Lock()
        self._redis_client = None  # redis client object

        self._key_high_priority = None
        self._key_low_priority = None
        self._set = None
        self._last_news_list = None

        self.init_redis()
        self._parse_queue = queue.PriorityQueue()
        self._save_queue = queue.Queue()
        self._proxies_queue = queue.Queue()

        # NUMBER OF IT
        self._number_dict = {
            FlagEum.TASKS_RUNNING: 0,

            FlagEum.URL_FETCH_NOT: 0,
            FlagEum.URL_FETCH_SUCC: 0,
            FlagEum.URL_FETCH_FAIL: 0,
            FlagEum.URL_FETCH_COUNT: 0,

            FlagEum.HTML_PARSE_NOT: 0,
            FlagEum.HTML_PARSE_SUCC: 0,
            FlagEum.HTML_PARSE_FAIL: 0,

            FlagEum.ITEM_SAVE_NOT: 0,
            FlagEum.ITEM_SAVE_SUCC: 0,
            FlagEum.ITEM_SAVE_FAIL: 0,

            FlagEum.PROXIES_LEFT: 0,
            FlagEum.PROXIES_FAIL: 0,
        }
        self.update_number_dict(FlagEum.URL_FETCH_NOT, -1)

        self._monitor_flag = True
        self._monitor = MonitorThread("monitor", self, sleep_time=monitor_sleep_time)
        self._monitor.setDaemon(True)
        self._monitor.start()

    def init_redis(self, host="localhost", port=6379, db=0, key_high_priority="spider.highList",
                   key_low_priority="spider.lowList"):
        """
        initial redis client object
        """
        if not self._redis_client:
            self._redis_client = redis.Redis(host=host, port=port, db=db)
        self._key_high_priority = key_high_priority
        self._key_low_priority = key_low_priority
        self._set = "urlSet"
        self._last_news_list = "last_news"

    def get_monitor_flag(self):
        return self._monitor_flag

    def get_number_dict(self, key):
        return self._number_dict[key]

    def get_proxies_flag(self):
        return True if self._proxieser else False

    def set_start_url(self, urls, priority=0):
        for url in urls:
            self._redis_client.srem(self._set, url) if self._redis_client.sismember(self._set, url) else None
            self.add_a_task(FlagEum.URL_FETCH, (priority, self.get_number_dict(FlagEum.URL_FETCH_COUNT), url, 0))
            print("%s set_start_url: %s" % (self.__class__.__name__,
                                            CONFIG_FETCH_MESSAGE % (priority, 0, url)))

    def start_work(self, fetcher_num=10, is_over=True):

        # ----proxies----
        # proxies_thread = ProxiesThread("Proxies", self._proxieser, self)
        # if proxies_thread:
        #     proxies_thread.setDaemon(True)
        #     proxies_thread.start()

        # ----fetch----
        fetcher_list = [FetchThread("fetcher-%d" % (i + 1), copy.deepcopy(self._inst_fetcher), self) for i in
                        range(fetcher_num)]
        for thread in fetcher_list:
            thread.setDaemon(True)
            thread.start()

        # ----parse and saver----
        parser = ParseThread("parser", self._inst_parser, self)
        saver = SaveThread("saver", self._inst_saver, self)
        parser.setDaemon(True)
        saver.setDaemon(True)
        parser.start()
        saver.start()

        # ----fetch join----
        for thread in fetcher_list:
            if thread.is_alive():
                thread.join()

        # clear the variables if all fetcher stoped
        while self.get_number_dict(FlagEum.URL_FETCH_NOT) > 0:
            priority, counter, url, repeat = self.get_a_task(FlagEum.URL_FETCH)

            print("%s error: not fetch, %s" % self._inst_fetcher.__class__.__name__,
                  CONFIG_FETCH_MESSAGE % (priority, repeat, url))
            self.update_number_dict(FlagEum.URL_FETCH_FAIL, +1)
            self.finish_a_task(FlagEum.URL_FETCH)

        # ----2----

        if parser.is_alive() or saver.is_alive():
            parser.join()
            saver.join()
        # ----3----
        if is_over and self._monitor.is_alive():
            self._monitor_flag = False
            self._monitor.join()

    def update_number_dict(self, key, value):
        self._lock.acquire()
        self._number_dict[key] += value
        self._lock.release()

    def add_a_task(self, task_name, task_content):
        if task_name == FlagEum.PROXIES:
            self._proxies_queue.put_nowait(task_content)
            self.update_number_dict(FlagEum.PROXIES_LEFT, +1)
        elif task_name == FlagEum.URL_FETCH and not self._redis_client.sismember(self._set, task_content[2]):

            self._redis_client.sadd(self._set, task_content[2])
            self._redis_client.rpush(self._key_high_priority, task_content) if task_content[
                                                                                   0] > 0 else self._redis_client.rpush(
                self._key_low_priority, task_content)
            self.update_number_dict(FlagEum.URL_FETCH_COUNT, +1)

        elif task_name == FlagEum.HTML_PARSE:
            self._parse_queue.put_nowait(task_content)
            self.update_number_dict(FlagEum.HTML_PARSE_NOT, +1)
        elif task_name == FlagEum.ITEM_SAVE:
            self._save_queue.put(task_content)
            self.update_number_dict(FlagEum.ITEM_SAVE_NOT, +1)

    def get_a_task(self, task_name):
        task_content = None

        if task_name == FlagEum.PROXIES:
            task_content = self._proxies_queue.get(block=True, timeout=5)
            self.update_number_dict(FlagEum.PROXIES_LEFT, -1)

        elif task_name == FlagEum.URL_FETCH:
            task_content = eval(
                self._redis_client.rpop(self._key_high_priority) or self._redis_client.rpop(self._key_low_priority))
        elif task_name == FlagEum.HTML_PARSE:
            task_content = self._parse_queue.get(block=True, timeout=5)
            self.update_number_dict(FlagEum.HTML_PARSE_NOT, -1)

        elif task_name == FlagEum.ITEM_SAVE:
            task_content = self._save_queue.get(block=True, timeout=5)
            self.update_number_dict(FlagEum.ITEM_SAVE_NOT, -1)

        self.update_number_dict(FlagEum.TASKS_RUNNING, +1)
        return task_content

    def finish_a_task(self, task_name):
        if task_name == FlagEum.PROXIES:
            self._proxies_queue.task_done()
            return
        elif task_name == FlagEum.URL_FETCH:
            pass
        elif task_name == FlagEum.HTML_PARSE:
            self._parse_queue.task_done()
        elif task_name == FlagEum.ITEM_SAVE:
            self._save_queue.task_done()
        self.update_number_dict(FlagEum.TASKS_RUNNING, -1)
        return

    def is_all_tasks_done(self):
        """
        check if all tasks are done, according to self._number_dict
        """
        return False if self._number_dict[FlagEum.TASKS_RUNNING] or self._number_dict[FlagEum.URL_FETCH_NOT] or \
                        self._number_dict[FlagEum.HTML_PARSE_NOT] or self._number_dict[FlagEum.ITEM_SAVE_NOT] else True

    def redis_operate(self, lsit_name, content):
        self._redis_client.lpush(lsit_name, content)
