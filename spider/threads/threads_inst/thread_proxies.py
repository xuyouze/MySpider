# coding: utf-8
import time

from . import BaseThread
from .thread_config import FlagEum


class ProxiesThread(BaseThread):
    def working(self):
        proxies_list = self._worker.working()

        for proxies in proxies_list:
            self._pool.add_a_task(FlagEum.PROXIES, proxies)

        while (self._pool.get_number_dict(FlagEum.PROXIES_LEFT) > 100) and (not self._pool.is_all_tasks_done()):
            print("%s[%s] sleep 5 seconds because of too many 'PROXIES_LEFT' ..." % (
                self.__class__.__name__, self.getName()))
            time.sleep(5)
            print(111)
        return True if not self._pool.is_all_tasks_done() else False
