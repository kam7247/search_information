import ssl

import ssl
import requests
import re
import pymorphy2
from bs4.element import Comment
from bs4 import BeautifulSoup

morph = pymorphy2.MorphAnalyzer()

def task2():
    ssl._create_default_https_context = ssl._create_unverified_context
    htmls = get_list_of_urls()
    tokens_file = open('task2/tokens.txt', 'w')
    lemmas_file = open('task2/lemmas.txt', 'w')
    tokens = set()
    for idx, url in enumerate(htmls):
        words = get_words(file_get_content('task1/urls/' + str(idx) + '.txt'))
        file_of_each_url_tokens = open('task2/tokens_' + str(idx) + '.txt', 'w')
        file_of_each_url_lemmas = open('task2/lemmas_' + str(idx) + '.txt', 'w')
        for word in words:
            word = word.lower()
            if (word not in tokens) and (is_not_trash(word)):
                tokens.add(word)
                tokens_file.write(word + '\n')
                file_of_each_url_tokens.write(word + '\n')
                lemmas = set_lema(word)
                for lem in lemmas:
                    lemmas_file.write('<' + lem + '>')
                    file_of_each_url_lemmas.write('<' + lem + '>')
                lemmas_file.write('\n')
                file_of_each_url_lemmas.write('\n')
        file_of_each_url_tokens.close()
        file_of_each_url_lemmas.close()
    tokens_file.close()
    lemmas_file.close()


def is_not_trash(word):
    return (morph.parse(word)[0].tag.POS != (
            'CONJ' or 'PREP' or 'PRCL' or 'INTJ' or 'ADVB' or 'ADVB' or 'PRED')
            and (word != ('еще' or 'ещё')))


def get_list_of_urls():
    with open("task1/url.txt") as file:
        array = [row.strip() for row in file]
    return array


def get_words(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    clean_text = filter(excluding_tags, texts)
    final_text = u" ".join(t.strip() for t in clean_text)
    return re.findall(r'[a-zA-ZА-Яа-яё]{3,}', final_text)


def excluding_tags(element):
    if (element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']) or (isinstance(element, Comment)):
        return False
    return True

def set_lema(token):
    lems = []
    for p in morph.parse(token):
        lems.append(p.normal_form)

    return list(set(lems))

def file_get_content(fileName):
    with open(fileName, 'r') as theFile:
        data = theFile.read()
        return data


if __name__ == '__main__':
    task2()
