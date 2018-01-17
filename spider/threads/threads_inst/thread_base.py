import queue
import threading
from ...util import *


class BaseThread(threading.Thread):
    def __init__(self, name, worker, pool):
        threading.Thread.__init__(self, name=name)
        self._worker = worker
        self._pool = pool

    def run(self):

        while True:
            try:
                self.working()
            except(queue.Empty, TypeError):
                if self._pool.is_all_tasks_done():
                    break

            except Exception:
                print("%s [%s] error:%s " % (self.__class__.__name__, self.getName(), get_error_info()))

    def working(self):
        raise NotImplementedError
