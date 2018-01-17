# coding:utf-8

import spider

if __name__ == '__main__':
    global url_dict
    url_dict = {}

    fetcher = spider.Fetch()
    proxieser = spider.Proxies()
    parser = spider.Parse()
    saver = spider.Saver()
    url_filter = spider.UrlFilter(url_dict)
    # web_spider = spider.WebSpider(fetcher=fetcher, proxieser=proxieser)
    web_spider = spider.WebSpider(fetcher=fetcher, parser=parser, saver=saver, url_filter=url_filter)
    web_spider.set_start_url(spider.NEWS_URL, priority=0)

    web_spider.start_work(fetcher_num=10, is_over=True)
