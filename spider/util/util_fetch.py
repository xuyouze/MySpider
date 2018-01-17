# coding: utf-8


import sys
import traceback
import re
import urllib.parse

__all__ = [
    "get_error_info",
    "get_url_params"
]


def get_error_info():
    """
        get error information from exception, return a string.
    :return: string
    """
    _type, _value, _trackback = sys.exc_info()
    tb_list = traceback.extract_tb(_trackback)
    error_info = "->".join(["[file=%s, line=%s, func=%s]" % (tb.filename, tb.lineno, tb.name) for tb in tb_list])
    return "error_info=%s, error_type=%s, error=%s" % (error_info, _type, _value)




def get_url_params(url, keep_blank_value=False, encoding="utf-8"):
    """
    get main_part(a string) and query_part(a dictionary) from a url
    """
    url_frags = urllib.parse.urlparse(url, allow_fragments=True)
    main_part = urllib.parse.urlunparse((url_frags.scheme, url_frags.netloc, url_frags.path, url_frags.params, "", ""))
    query_part = urllib.parse.parse_qs(url_frags.query, keep_blank_values=keep_blank_value, encoding=encoding)
    return main_part, query_part
