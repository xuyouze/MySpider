from enum import Enum

__all__ = [
    "FlagEum"
]


class FlagEum(Enum):
    TASKS_RUNNING = "tasks_running"

    # fetch flag
    URL_FETCH = "url_fetch"
    URL_FETCH_NOT = "url_fetch_not"
    URL_FETCH_SUCC = "url_fetch_succ"
    URL_FETCH_FAIL = "url_fetch_fail"
    URL_FETCH_COUNT = "url_fetch_count"

    # parse
    HTML_PARSE = "html_parse"
    HTML_PARSE_NOT = "htm_parse_not"
    HTML_PARSE_SUCC = "htm_parse_succ"
    HTML_PARSE_FAIL = "htm_parse_fail"

    ITEM_SAVE = "item_save"  # flag of item_save
    ITEM_SAVE_NOT = "item_save_not"  # flag of item_save_not
    ITEM_SAVE_SUCC = "item_save_succ"  # flag of item_save_succ
    ITEM_SAVE_FAIL = "item_save_fail"  # flag of item_save_fail

    PROXIES = "proxies"  # flag of proxies
    PROXIES_LEFT = "proxies_left"  # flag of proxies_left --> URL_FETCH_NOT
    PROXIES_FAIL = "proxies_fail"  # flag of proxies_fail --> URL_FETCH_FAIL
