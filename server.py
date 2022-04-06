#!/usr/bin/env python3

# запускает web-сервер на порту 8080
# со скриптами в cgi-bin

import http.server

port = 8080

addrport = ('', port)

serv = http.server.HTTPServer(
    addrport,
    http.server.CGIHTTPRequestHandler
)
serv.serve_forever()
