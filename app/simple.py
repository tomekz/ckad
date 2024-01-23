#!/usr/bin/python

import time
import socket

while True:
    host = socket.gethostname()
    date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    now = str(date)

    f = open('date.out', 'a')
    f.write(host + ' ' + now + '\n')
    f.close()

    time.sleep(5)
