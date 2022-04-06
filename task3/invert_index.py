import re
import ssl
import string
import zipfile
from functools import cmp_to_key
import pymorphy2
import nltk
from bs4 import BeautifulSoup


class WordsCount:
    def __init__(self):
        self.documents = []
        self.general_count = 0

    def append_document_info(self, document_number, document_word_count):
        self.documents.append(document_number)
        self.general_count += document_word_count


def tokenizator(html):
    page_content = BeautifulSoup(html, features="html.parser").get_text()
    result = list(nltk.wordpunct_tokenize(page_content))
    return result


def minus_znak_prep(values):
    return [i for i in values if all(not j in string.punctuation for j in i)]


def minus_incorrect_sym(word):
    rus = re.compile(r'^[а-яА-Я]{2,}$')
    numbers = re.compile(r'^[0-9]+$')
    res = bool(rus.match(word)) or bool(numbers.match(word))
    return res


def get_lemma(word):
    p = pymorphy2.MorphAnalyzer().parse(word)[0]
    if p.normalized.is_known:
        normal_form = p.normal_form
    else:
        normal_form = word.lower()
    return normal_form


def get_lemmas():
    f = open("/Users/berendakova/PycharmProjects/search_info/task2/lemmas.txt", "r")
    lines = f.readlines()
    lemmas = dict()
    for line in lines:
        key = None
        words = re.split('\s+', line)
        for i in range(len(words) - 1):
            if i == 0:
                key = words[i]
                lemmas[key] = []
            else:
                lemmas[key].append(words[i])
    return lemmas


def get_doc_id(filename):
    id = ""
    for letter in filename:
        if letter.isdigit():
            id += letter
    return int(id)


def sort_id(id):
    def comparator(x, y):
        return x[1].general_count - y[1].general_count

    return dict(sorted(id.items(), key=cmp_to_key(comparator), reverse=True))


def get_list_of_urls():
    with open("/Users/berendakova/PycharmProjects/search_info/task1/url.txt") as file:
        array = [row.strip() for row in file]
    return array


def get_words(map):
    ssl._create_default_https_context = ssl._create_unverified_context
    urls = get_list_of_urls()
    index = dict()
    for idx, url in enumerate(urls):
        html = file_get_content('/Users/berendakova/PycharmProjects/search_info/task1/urls/' + str(idx) + '.txt')
        html_word_list = tokenizator(html)
        word_used = set()
        for word in html_word_list:
            lemma = '<' + get_lemma(word) + '>'
            if lemma in map.keys() and lemma not in word_used:
                word_used.add(lemma)
                similar_words = map[lemma]
                count = 0
                for similar_word in similar_words:
                    count += html_word_list.count(similar_word)
                if lemma not in index.keys():
                    index[lemma] = WordsCount()
                index[lemma].append_document_info(str(idx), count)
        print(idx, "finished")
    return dict(sorted(index.items()))


def set_answers(index):
    file = open("../cgi-bin/index.txt", "w")
    for word, doc_info in index.items():
        file_string = word + " "
        for doc in doc_info.documents:
            file_string += " " + str(doc)
        file_string += "\n"
        file.write(file_string)
    file.close()

def file_get_content(fileName):
    with open(fileName, 'r') as theFile:
        data = theFile.read()
        return data

def read_index():
    f = open("/cgi-bin/idx_urls.txt", "r")
    lines = f.readlines()
    map = dict()
    for line in lines:
        words = re.split('\s+', line)
        key = words[0]
        if not key in map.keys():
            map[key] = set()
        for i in range(1, len(words) - 1):
            map[key].add(words[i])
    return map


def boolean_search(need_word, index):
    word = '<' + need_word + '>'
    query_words = re.split('\s+', word)
    page_crossing = set()
    token_query = set(map(lambda x: get_lemma(x),  query_words))
    for word in token_query:
        page_crossing = page_crossing | index[word]
    print(page_crossing)


if __name__ == '__main__':
    lemmas = get_lemmas()
    index = get_words(lemmas)
    sorted_index = sort_id(index)
    set_answers(sorted_index)
    boolean_search("актёр", read_index())