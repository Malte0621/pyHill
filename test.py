# PyHill - A brick-hill client in python, by Malte0621. #

import configparser
import time
import os
import sys
import random
import math
import requests
import socket
import psutil
from connector import Connector
from termcolor import cprint


def intify(s):
    try:
        return int(s)
    except:
        return None


def main():
    connector_dest_port = input("Connector Destination Port (1621): ")
    if connector_dest_port.strip() == "":
        connector_dest_port = 1621
    else:
        connector_dest_port = intify(connector_dest_port)
        if connector_dest_port is None:
            cprint("Invalid port.", "red")
            return
    fp = os.path.join(os.getcwd(), "token.txt")
    if os.path.exists(fp) and False:
        f = open(fp, "r+")
        cookie = f.read().strip()
        f.close()
    else:
        cookie = input("X-CSRF-TOKEN OR TOKEN: ") or "local"
    setId = intify(input("SetID: ")) or 1
    ip = input("IP: ") or "127.0.0.1"
    port = intify(input("PORT: ")) or 42480
    connector = Connector(cookie, setId, ip, port, connector_dest_port=connector_dest_port)

    conn = None

    def chat_cb(message):
        message = message.decode(errors="ignore")
        print(message)
        if message.startswith("<color:FFD814>[NOTICE]: This server is proudly hosted with node-hill"):
            if conn is not None:
                time.sleep(1)
                conn.chat("Hello from the pyHill client!".encode())

    connector.set_callback("chat", chat_cb)

    conn = connector.connect()

    time.sleep(2)

    for i in range(5):
        time.sleep(3)
        if conn is not None:
            conn.chat("Moving..".encode())
            conn.move(0, 0, random.randint(100, 250))
    conn.disconnect()


if __name__ == '__main__':
    main()
