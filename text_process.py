# coding=utf-8
# -*- coding: cp936 -*-
import jieba
import jieba.posseg as pseg
import codecs
import re
import os
import time
import string
import wordcloud
from nltk.probability import FreqDist
open=codecs.open

#定义一个keyword类
class keyword(object):
    def Chinese_Stopwords(self):          #导入停用词库
        stopword=[]
        cfp=open('stopWord.txt','r+','utf-8')   #停用词的txt文件
        for line in cfp:
            for word in line.split():
                stopword.append(word)
        cfp.close()
        return stopword

    def Word_cut_list(self,word_str):
        #利用正则表达式去掉一些一些标点符号之类的符号。
        word_str = re.sub(r'\s+', ' ', word_str)  # trans 多空格 to空格
        word_str = re.sub(r'\n+', ' ', word_str)  # trans 换行 to空格
        word_str = re.sub(r'\t+', ' ', word_str)  # trans Tab to空格
        word_str = re.sub(r"[\s+\.\!\/_,$%^*(+\"\']+|[+——；！，”。《》，。：“？、~@#￥%……&*（）1234567①②③④)]+", "", word_str)
  
        wordlist = list(jieba.cut(word_str))#jieba.cut  把字符串切割成词并添加至一个列表
        wordlist_N = []
        chinese_stopwords=self.Chinese_Stopwords()
        for word in wordlist:
            if word not in chinese_stopwords:#词语的清洗：去停用词
                if word != '\r\n'  and word!=' ' and word != '\u3000' \
                        and word!='\xa0':#词语的清洗：去全角空格
                    wordlist_N.append(word)
        return wordlist_N

    def Word_pseg(self,word_str):  # 名词提取函数
        words = pseg.cut(word_str)
        word_list = []
        for wds in words:
            # 筛选自定义词典中的词，和各类名词，自定义词库的词在没设置词性的情况下默认为x词性，即词的flag词性为x
            if wds.flag == 'x' and wds.word != ' ' and wds.word != 'ns' \
                    or re.match(r'^n', wds.flag) != None \
                            and re.match(r'^nr', wds.flag) == None:
                word_list.append(wds.word)
        return word_list

    def sort_item(self,item):#排序函数，正序排序
        vocab=[]
        for k,v in item:
            vocab.append((k,v))
        List=list(sorted(vocab,key=lambda v:v[1],reverse=1))
        return List

    def Run(self):
        Apage=open(self.filename,'r+','utf-8')
        Word=Apage.read()                       #先读取整篇文章
        Wordp=self.Word_pseg(Word)              #对整篇文章进行词性的挑选
        New_str=''.join(Wordp)
        Wordlist=self.Word_cut_list(New_str)    #对挑选后的文章进行分词
        Apage.close()
        return  Wordlist

    def __init__(self, filename):
        self.filename = filename

class SummaryInformation():
    def __init__(self):
        with open("FROM.txt",'r','utf-8') as f:
        # 行数
            self.cnt_from = len(f.readlines())
            self.word_from = len(open("FROM.txt",'r','utf-8').read().rstrip())
        with open("TO.txt",'r','utf-8') as f:
            self.cnt_to = len(open("TO.txt", "r",'utf-8').readlines())
            # 字数
            self.word_to = len(open("TO.txt",'r','utf-8').read().rstrip())
    def 

if __name__=='__main__':
    # 行数
    cnt_from = len(open("FROM.txt",'r','utf-8').readlines())
    cnt_to = len(open("TO.txt", "r",'utf-8').readlines())
    # 字数
    word_from = len(open("FROM.txt",'r','utf-8').read().rstrip())
    word_to = len(open("TO.txt",'r','utf-8').read().rstrip())
    if cnt_from < cnt_to:
        print("你给ta发送了{}条消息，而ta给你发送了{}条消息".format(cnt_to, cnt_from))
        print("你的总字数为{}, ta的总字数为{}".format(word_to, word_from))
        print("你给ta的消息平均字数为{:.3}, 而ta给你消息平均字数为{:.3}".format(word_to/cnt_to, word_from/cnt_from))
    else:
        print("ta给你发送了{}条消息，而你给ta发送了{}条消息".format(cnt_from, cnt_to))
        print("ta的总字数为{}, 你的总字数为{}".format(word_from, word_to))
        print("ta给你的消息平均字数为{:.3}, 而你给ta消息平均字数为{:.3}".format(word_from/cnt_from, word_to/cnt_to))

    print("---------")
    files = ["FROM.txt", "TO.txt"]
    for file in files:
        kw = keyword(file)
        wl = kw.Run()
        # 构建词云对象w，设置词云图片宽、高、字体、背景颜色等参数
        w = wordcloud.WordCloud(width=1000,
                                height=700,
                                background_color='white',
                                font_path='msyh.ttc')
        txt = " ".join(wl)
        w.generate(txt)
        # 将词云图片导出到当前文件夹
        w.to_file("wordcloud_"+file[:-4]+'.png')
    