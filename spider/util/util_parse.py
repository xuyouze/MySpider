# coding:utf-8
import re

__all__ = [
    "parse_content",
    "replace"
]


def parse_content(url, soup):
    if "163" in url:
        return stratege_netease(soup)
    elif "ifeng" in url:
        return strategy_ifeng(soup)


def strategy_ifeng(soup):
    date_tag = [
        "#artical span[itemprop='datePublished']",
        "#titL span", "div .stoBigPicCon span",
        "div .imgDate pcdn",
        "div[class='yc_tit'] span"
        "div[class='yc_tit'] span",
        "span[class='Arial']"
    ]

    source_tag = [
        "#artical span[itemprop='publisher']",
        "p[class='cGray2'] span a",
        "div[class='yc_tit'] a"
    ]

    content_tag = [
        "#main_content",
        "div[class='yc_con_txt'] p",
        "div[class='wrapIphone AtxtType01'] p",
        "div[class='fl stoConLef'] p"
    ]

    title_tag = [
        "#artical_topic", "#titL h1",
        "div[class='stoBigPicCon'] h1",
        "div[class='imgTit pcdn']",
        "div[class='yc_tit h1']",
        "head title"
    ]

    return search(date_tag, soup), search(source_tag, soup), search(title_tag, soup), search_content(content_tag, soup)


def stratege_netease(soup):
    date_tag = [
        "div[class='post_time_source']", "#ptime", "div[class='pub_time']"
    ]
    source_tag = [
        "#ne_article_source"
    ]
    title_tag = [
        "#epContentLeft h1", "div[class='left'] h1", "div[class='bannertext'] h1", "div[class='brief'] h1"
    ]
    content_tag = [
        "#endText p"
    ]
    return search(date_tag, soup), search(source_tag, soup), search(title_tag, soup), replace(
        search_content(content_tag, soup))


def search(items, soup):
    for i in items:
        if soup.select(i):
            return soup.select(i)[0].text

    return ""


def search_content(item, soup):
    for i in item:
        if soup.select(i):
            return " ".join([x.text for x in soup.select(i)])


def replace(content):
    r = re.compile(
        r'(<script.*</script>|'
        r'<style.*?</style>|'
        r'<!--.*?-->|'
        r'<meta.*>|'
        r'<ins.*</ins>|'
        r'define.*?\);|'
        r'//.*数据|'
        r'<[^>]+>|'
        r'^\s+$|'
        r'\n+|'
        r'\s+|#end.*\})',
        re.I | re.M | re.S)  # 删除JavaScript
    return r.sub('', content)
