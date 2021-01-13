#!/usr/bin/env python3

import sys
import threading
import random, string
import datetime

def timestr():
    return datetime.datetime.now().strftime("[%y-%m-%d %H:%M:%S]")

def log(text):
    text = timestr() + " " + text
    
    with log.lock:
        # log to stdout
        print(text)
        sys.stdout.flush()

        # log to file
        f = open("main.log", "a")
        f.write(text)
        f.write("\n")
        f.close()

# static variable for multi-thread locking of logger
# has to be defined only after function log.
log.lock = threading.Lock()

