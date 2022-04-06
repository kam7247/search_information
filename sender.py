#!/usr/bin/env python3

# посылает запрос на выполнение скрипта на сервере

import urllib.request

url = 'http://localhost:8080/cgi-bin/script.py'

req = urllib.request.Request(url)

with urllib.request.urlopen(req) as data:
    charset = data.headers.get_content_charset()
    page = data.read().decode(charset or 'latin1')

print(page)
