import ssl
import requests
import re
import pymorphy2
from bs4.element import Comment
from bs4 import BeautifulSoup

morph = pymorphy2.MorphAnalyzer()

def task1():
    with open("task1/url.txt") as file:
        array = [row.strip() for row in file]
    print(len(array))
    index = open('cgi-bin/idx_urls.txt', 'w')
    for idx, el in enumerate(array):
        print(el)
        url = 'https://' + el
        send = requests.post(url)
        filename = 'task1/urls/' + str(idx) + '.txt'
        file = open(filename, 'wb')
        file.write(send.text.encode('utf-8'))
        index.write(str(idx) + ' ' + el + '\n')
        file.close()

    index.close()

if __name__ == '__main__':
    task1()
