# coding: utf-8
import jieba
from gensim import corpora, models
from .news import News
from ..util.util_fetch import get_error_info
import os


class Saver(object):
    def __init__(self):
        self.stopwords = {}
        self.get_stop_word()
        self.dictionary = corpora.Dictionary.load('spider/weight/lda_dict.dic')  # 加载字典
        self.lda = models.LdaModel.load('spider/weight/lda.pkl')  # LDA model 的使用

    def get_stop_word(self):
        print(os.getcwd())
        fstop = open('spider/instances/stopword.txt', 'r', encoding="utf-8")
        for eachWord in fstop:
            self.stopwords[eachWord.strip()] = eachWord.strip()
        fstop.close()

    def working(self, news: News) -> (bool, News):
        print("%s start: title: %s, url:%s" % (self.__class__.__name__, news.news_title, news.news_url))
        news_split = None
        flag = False
        try:
            flag, news_split = self.doc_process(news)
        except Exception:
            print("%s error: %s, %s" % (self.__class__.__name__, get_error_info(), news.news_title))

        print("%s end: save_result=%s, title=%s, url=%s" % (
            self.__class__.__name__, flag, news.news_title, news.news_url))
        return flag, news_split

    def doc_process(self, news):

        # 分词
        wordList = jieba.lcut(news.news_content)  # 用结巴分词，对每行内容进行分词
        news_content_list = [x for x in wordList if x not in self.stopwords]
        news.news_content = " ".join(news_content_list[:150] if len(news_content_list) > 150 else news_content_list)

        # 输出新文档的主题分布
        doc_bow = self.dictionary.doc2bow(news_content_list)  # 文档转换成bow
        doc_lda = self.lda[doc_bow]  # 得到新文档的主题分布
        d = {key: value for (key, value) in doc_lda}
        for x in range(10):
            if x not in d.keys():
                d[x] = 0
        news.news_topic_vec = d
        print(d)

        return 1, news
