# coding: utf-8
from .thread_config import FlagEum
from .thread_base import BaseThread
from ...util.util_config import save_list


class SaveThread(BaseThread):
    """
    class of SaveThread, as the subclass of BaseThread
    """

    def working(self):
        """
        procedure of saver, auto running, and only return True
        """
        # ----1----
        # (priority, counter, url, content)
        news = self._pool.get_a_task(FlagEum.ITEM_SAVE)

        # ----2----
        #
        save_result, news = self._worker.working(news)
        # ----3----
        if save_result:
            self._pool.update_number_dict(FlagEum.ITEM_SAVE_SUCC, +1)
            self._pool.redis_operate(save_list, news)
        else:
            self._pool.update_number_dict(FlagEum.ITEM_SAVE_FAIL, +1)

        # ----4----
        self._pool.finish_a_task(FlagEum.ITEM_SAVE)
        return True
