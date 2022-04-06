#!/usr/bin/env python3

# выводит html-страницу с ответом из формы

import cgi
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk
from pymorphy2 import MorphAnalyzer
import numpy as np
import re
from string import punctuation
from scipy import spatial

form = cgi.FieldStorage()

print('Content-type: text/html')
print()


title = 'Reply Page'

before = """
<html>
  <head>
    <meta http-equiv='Content-Type' content='text/html; charset=utf-8'>
    <title>{}</title>
  </head>
  <body>
""".format(title)

after = """
  </body>
</html>
"""

namefmt = '<h1>Hello <i>{}</i>!</h1>'

noname = '<h1>Who are you?</h1>'


print(before, end='')


class VectorModel:
    def __init__(self):
        self.lemmas, self.matrix = self.load_index()
        nltk.download('punkt')
        nltk.download('stopwords')
        self.pymorphy2_analyzer = MorphAnalyzer()

    def load_index(self):
        with open('/Users/berendakova/PycharmProjects/search_info/cgi-bin/index.txt', 'r', encoding='utf-8') as file:
            lines = file.readlines()

        lemmas_list = list()
        matrix = [[0] * 100 for _ in range(len(lines))]
        for idx, line in enumerate(lines):
            line = re.sub('\n', '', line)
            lemma = line.split(': ')[0]
            lemmas_list.append(lemma)
            pages = line.split(': ')[1].split(', ')
            for page in pages:
                matrix[idx][int(page) - 1] = 1

        return lemmas_list, np.array(matrix).transpose()

    def is_valid(self, token, stop_words, stop_symbols):
        valid = True
        if token in stop_words:
            valid = False
        elif token in stop_symbols:
            valid = False
        elif token.isdigit():
            valid = False
        elif re.match('[1-9]+,[0-9]+', token) is not None:
            valid = False
        elif re.match('^([0-9]|0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$', token) is not None:
            valid = False

        try:
            num = float(token)
            if num:
                valid = False
        except ValueError:
            pass

        return valid

    def get_vector(self, search_string):
        stop_words = stopwords.words('russian')
        stop_symbols = [symbol for symbol in punctuation]
        stop_symbols += ['№', '«', '»', '—']

        search_tokens = word_tokenize(search_string)
        search_tokens = [line_token.lower() for line_token in search_tokens]
        cleaned_search_tokens = [line_token for line_token in search_tokens if
                                 self.is_valid(line_token.lower(), stop_words, stop_symbols)]

        tokens_normal_form = [self.pymorphy2_analyzer.parse(token)[0].normal_form for token in cleaned_search_tokens]
        vector = [0] * len(self.lemmas)
        for token in tokens_normal_form:
            if token in self.lemmas:
                vector[self.lemmas.index(token)] = 1

        return vector

    def search(self, search_string):
        vector = self.get_vector(search_string)

        docs = dict()
        for idx, doc in enumerate(self.matrix):
            if max(doc) == 1:
                docs[idx + 1] = 1 - spatial.distance.cosine(vector, doc)
            else:
                docs[idx + 1] = 0.0

        sorted_docs = sorted(docs.items(), key=lambda x: x[1], reverse=True)

        return sorted_docs


if 'user' in form:
    vector = VectorModel()
    urls = vector.search(form['user'].value)
    file1 = open("/Users/berendakova/PycharmProjects/search_info/cgi-bin/idx_urls.txt", "r")
    line = file1.readlines()
    for url in urls:
        if url[1] > 0 :
            for l in line :
                idx = l.split(' ')
                string = ''
                if int(idx[0]) == int(url[0]):
                    string += "<p>" + str(idx[1]) + "</p>" + " " + str(url[1])+ '\n'
                    print(string)


print(after, end='')
