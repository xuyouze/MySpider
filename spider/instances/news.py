class News(object):
    """
    :source 哪里找到的
    :title: 标题
    :time: 时间
    :url: 路径
    :type :类型
    :keyword 关键字

    """

    def __init__(self, source: str, title: str, time: str, url: str, content: str, topic_vec=None, keyword=None,
                 news_id=None):
        self.news_id = news_id
        self.news_source = source
        self.news_title = title
        self.news_time = time
        self.news_topic_vec = topic_vec
        self.news_keyword = keyword
        self.news_url = url
        self.news_content = content

    def __str__(self, *args, **kwargs):
        return str(dict((name, getattr(self, name)) for name in dir(self)
                        if not name.startswith('__') and not callable(self)))
