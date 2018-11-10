# -*- coding: utf-8 -*-
import re
import numpy as np


class Segmentation:
    dictPath = ''
    delimiter = ",|\s+|,\s|\s"
    Dict = []

    def __init__(self, dictName=None):
        if dictName != None:
            self.dictPath = dictName
            self.load_Dict()

    def load_Dict(self):
        ans = []
        with open(self.dictPath, 'r', encoding='utf-8') as dict_file:
            lines = dict_file.readlines()
            for line in lines:
                sp = re.split(self.delimiter, line.strip())
                ans.extend(sp)
                # print(sp)
        ans = list(set(ans))
        ans.remove('')
        ans.remove('none.')
        self.Dict = ans

    def isExsit(self, word):
        return word in self.Dict

    # 前向最大匹配
    def FMM(self, sentence):
        L = len(sentence)
        words = []
        st = 0
        while st < L:
            for ed in range(L, st, -1):
                substr = sentence[st:ed]
                if len(substr) == 1 or (self.Dict and substr in self.Dict):
                    words.append(substr)
                    st = ed
                    break

        return words

    # 后向最大匹配
    def RMM(self, sentence):
        L = len(sentence)
        words = []
        ed = L
        while ed > 0:
            for st in range(0, ed):
                substr = sentence[st:ed]
                if len(substr) == 1 or (self.Dict and substr in self.Dict):
                    words.append(substr)
                    ed = st
                    break
        # print("RMM")
        # print(words)
        # print("reverse:")
        # print(words.reverse())
        words.reverse()
        return words

    # 双向最大匹配
    def BMM(self, sentence):  # 总词数、单个词数、非字典词越少越好
        #sentence_copy = sentence
        f_words = self.FMM(sentence)
        print("前向最大匹配分词结果:")
        print(f_words)
        # print(sentence)
        r_words = self.RMM(sentence)
        print("后向最大匹配分词结果:")
        print(r_words)
        f_len = len(f_words)
        r_len = len(r_words)

        # 统计长度为1的单个词数的个数
        def sum_single(x): return [len(i) for i in x].count(1)
        f_single, r_single = sum_single(f_words), sum_single(r_words)

        # 统计词典不存在的词的个数
        def sum_exsit(x): return [i in self.Dict for i in x].count(False)
        f_exsit, r_exsit = sum_exsit(f_words), sum_exsit(r_words)

        # 为了消除歧义，总词数、单个词数、非字典词越少越好，我们简单加和，取小者
        f_score = f_len + f_single + f_exsit
        r_score = r_len + r_single + r_exsit
        #print('%d %d' % (f_score, r_score))

        b_words = f_words if f_score <= r_score else r_words

        return b_words


def main():
    d = Segmentation('dic_ec.txt')
    # print(d.Dict)
    test_sentence = input("请输入中文句子:")
    words = d.BMM(test_sentence)
    print("双向最大匹配分词结果:")
    print(words)


if __name__ == '__main__':
    while True:
        main()
