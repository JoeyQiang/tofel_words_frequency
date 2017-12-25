# 托福作文词频统计

import re, collections
from bs4 import BeautifulSoup
import numpy as np
import matplotlib.pyplot as plt


# 过滤单词尾部的,.?"和头部的"
def filter_puctuation(word):
    return re.sub(r'(\,$)|(\.$)|(\?$)|(\"$)|(^\")', '', word)


def fileter_simple_words(words):
    # 过滤词清单
    simple_words = ['the', 'a', 'an', 'to', 'is',
                    'am', 'are', 'the', 'that', 'which',
                    'i', 'you', 'he', 'she', 'they',
                    'it', 'of', 'for', 'have', 'has',
                    'their', 'my', 'your', 'will', 'all',
                    'but', 'while', 'with', 'only', 'more',
                    'who', 'should', 'there', 'can', 'might',
                    'could', 'may', 'be', 'on', 'at',
                    'after', 'most', 'even', 'and', 'in',
                    'best', 'better', 'as', 'no', 'ever',
                    'me', 'not', 'his', 'her'
                    ]

    # words type is counter.
    for word in list(words):
        if word in simple_words:
            del words[word]

    return words


def filter_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    # 需要过滤<title>标签，避免作文题目干扰
    text = soup.body.get_text()
    return text


def calculate_words_frequency(file):
    # 读取文件
    with open(file) as f:
        # html 处理
        f = filter_html(f)

        line_box = []
        word_box = []

        # 转成小写并将句子分成词
        line_box.extend(f.strip().lower().split())

        # 去除标点符号的影响
        for word in line_box:
            if not word.isalpha():
                word = filter_puctuation(word)
            word_box.append(word)

        # 统计词频
        word_box = fileter_simple_words(collections.Counter(word_box))

        return word_box


def multiple_file_frequency(files):
    total_counter = collections.Counter()
    for file in files:
        total_counter += calculate_words_frequency(file)
    return total_counter


def most_common_words(files, number):
    total_counter = multiple_file_frequency(files)
    return total_counter.most_common(number)


def draw_figures(figures):
    labels, values = zip(*figures)
    indexes = np.arange(len(labels))
    width = 0.5
    plt.bar(indexes, values, width)
    plt.xticks(indexes, labels)
    plt.show()


files = ['Data/article_01.html', 'Data/article_02.html', 'Data/article_03.html', 'Data/article_04.html',
         'Data/article_05.html']

print(draw_figures(most_common_words(files, 10)))
