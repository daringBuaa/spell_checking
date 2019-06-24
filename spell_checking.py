# -*- coding: utf-8 -*-
import pandas as pd
import re
from sklearn.feature_extraction.text import CountVectorizer
import os

if os.path.exists('words.csv'):
    words_df = pd.read_csv('words.csv')
else:
    # 读取语义文件，统计词频作为改正的根据
    with open('big.txt') as f:
        text = f.read()
    # 通过正则找出所有单词
    all_words = re.findall('[a-z]+', text.lower()) # 忽略大小写
    # print(len(all_words)) 1091250
    myfile = ' '.join(all_words)  # 将其转化为空格分隔的文件，方便使用sklearn统计
    count = CountVectorizer()
    words_df = pd.DataFrame(count.fit_transform([myfile]).toarray(),columns=count.get_feature_names()) # 得到单词与对应频数的dataframe
    # 存储语义库，下次直接加载
    words_df.to_csv('words.csv')
words_dic = words_df.to_dict(orient='record')[0] # 转化后为每行一个字典组成的列表
# value_to_word_dict = {v:k for k,v in words_dic.items()}  # 可能出现多个键对应统一个值
# print(value_to_word_dict)

def word_edit1(word):
    # 输出word编辑距离为1的词库
    n = len(word)
    letter_str = 'abcdefghijklmnopqrstuvwxyz'
    result = list(set(
        [word[0:i]+word[i+1:] for i in range(n) ] +  # 删除一个字母
        [word[0:i] + word[i+1] + word[i] + word[i+2:] for i in range(n-1)]+ # 改一个字母的顺序
        [word[0:i]+c+word[i+1:] for i in range(n) for c in letter_str]+ # 改一个字母
        [word[0:i]+c+word[i:] for i in range(n) for c in letter_str]  # 增一个字母
    ))
    return result

def word_edit2(word):
    word1 = word_edit1(word)
    result = list()
    for w in word1:
        result += word_edit1(w)
    return result

def output(check_list):
    value_list = [words_dic[key] for key in check_list]
    candidate = check_list[value_list.index(max(value_list))] if len(value_list) else None
    return candidate

# 输入待检查单词，若出现在语言词库中则直接输出，否则逐步检查编辑距离1-2的词库
def correct(word):
    if word in words_dic.keys():
        return word
    # 检查编辑距离为1对应的词库
    check_list1 = word_edit1(word)
    # 只需检查词库中存在的词
    check_list1 = [i for i in check_list1 if i in words_dic.keys()]
    candidate =output(check_list1)
    if candidate:
        return candidate
    # 检查编辑距离为2的库
    check_list2 = word_edit2(word)
    check_list2 = [i for i in check_list2 if i in words_dic.keys()]
    candidate = output(check_list2)
    if candidate:
        return candidate
    else:
        return word



if __name__ == '__main__':
    while True:
        input_word = input("请输入单词：(输入stop结束)")
        if input_word == 'stop':
            break
        print(correct(input_word))