# coding: utf-8
import pandas as pd
from wordcloud import WordCloud
import jieba
import numpy
import PIL.Image as Image

df = pd.read_csv('C:/Users/Jeffrey/Desktop/chuli/group_1.csv', encoding='utf-8')
df.columns = ['0','content','date','time','user_id']
# print(df.head())
df = df[0:100]


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import jieba

# jieba.load_userdict('userdict.txt')
# 创建停用词list
def stopwordslist(filepath):
    stopwords = [line.strip() for line in open(filepath, 'r', encoding='utf-8').readlines()]
    return stopwords

# 对句子进行分词
def seg_sentence(sentence):
    sentence_seged = jieba.cut(sentence.strip())
    stopwords = stopwordslist('stop_words_cn.txt')  # 这里加载停用词的路径
    outstr = ''
    for word in sentence_seged:
        if word not in stopwords:
            if word != '\t':
                outstr += word
                outstr += " "
    return outstr




for line in df['content']:
    line_seg = seg_sentence(line)  # 这里的返回值是字符串
    print(line_seg)
    print("******")


