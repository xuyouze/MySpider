# coding: utf-8
from .thread_config import FlagEum
from .thread_base import BaseThread


class ParseThread(BaseThread):
    """
    class of ParseThread, as the subclass of BaseThread
    """

    def working(self):
        """
        procedure of parsing, auto running, and only return True
        """
        # ----1----
        # (priority, counter, url, content)
        priority, counter, url, content = self._pool.get_a_task(FlagEum.HTML_PARSE)

        # ----2----
        #  working(self, priority: int, url: str, repeat: int, content: object) -> (bool, News):
        parse_result, news = self._worker.working(priority, url, content)
        # ----3----
        if parse_result:
            self._pool.update_number_dict(FlagEum.HTML_PARSE_SUCC, +1)
            self._pool.add_a_task(FlagEum.ITEM_SAVE, news)
        else:
            self._pool.update_number_dict(FlagEum.HTML_PARSE_FAIL, +1)

        # ----4----
        self._pool.finish_a_task(FlagEum.HTML_PARSE)
        return True
