# PyHill - A brick-hill client in python, by Malte0621. #
# - Connector : Main connector that handles packets.
import json
import socket
import threading
from .helpers2 import *


class Connector:
    def __init__(self, cookie, setid, ip, port, connector_dest_port=1621):
        self.sobj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sobj.connect(('127.0.0.1', connector_dest_port))
        self.cbs = {
            "all": None,

            "auth": None,
            "newbricks": None,
            "brick": None,
            "playermod": None,
            "chat": None,
            "newplayer": None,
            "movement": None,
            "figure": None,
        }

        packet = Packet(0)
        if type(cookie) == str:
            cookie = cookie.encode()
        packet.write_string(cookie)
        packet.write_uint32(setid)
        if type(ip) == str:
            ip = ip.encode()
        packet.write_string(ip)
        packet.write_uint16(port)
        packet.compress()
        send_msg(self.sobj, packet.buffer)

        def t(self):
            while True:
                data = recv_msg(self.sobj)
                packet = Packet(data)
                try:
                    packet.decompress()
                except:
                    pass
                packetId = packet.read_uint8()
                if packetId == 255:
                    cb_name = packet.read_string().decode(errors="ignore")
                    args = packet.read_uint32()
                    args_out = []
                    for x in range(args):
                        t = packet.read_string().decode(errors="ignore")
                        if t == "str":
                            args_out.append(packet.read_string())
                        elif t == "int":
                            args_out.append(packet.read_long())
                        elif t == "float":
                            args_out.append(packet.read_float())
                        elif t == "list/dict":
                            args_out.append(json.loads(packet.read_string()))
                    try:
                        self.cbs[cb_name](*args_out)
                    except:
                        pass

        threading.Thread(target=t, args=[self]).start()

    def set_callback(self, cb_name, func):
        if not callable(func):
            return False
        if cb_name in self.cbs.keys():
            self.cbs[cb_name] = func
            packet = Packet(255)
            if type(cb_name) == str:
                cb_name = cb_name.encode()
            packet.write_string(cb_name)
            packet.compress()
            send_msg(self.sobj, packet.buffer)
            return True
        return False

    def connect(self):
        packet = Packet(1)
        packet.compress()
        send_msg(self.sobj, packet.buffer)

        def chat(message):
            packet = Packet(2)
            packet.write_string(message)
            packet.compress()
            send_msg(self.sobj, packet.buffer)

        def command(cmd, args):
            packet = Packet(3)
            packet.write_string(cmd)
            packet.write_string(args)
            packet.compress()
            send_msg(self.sobj, packet.buffer)

        def move(x, y, z, xr=0, xy=0):
            packet = Packet(4)
            packet.write_float(x)
            packet.write_float(y)
            packet.write_float(z)
            packet.write_float(xr)
            packet.write_float(xy)
            packet.compress()
            send_msg(self.sobj, packet.buffer)

        def player_input(click, key):
            packet = Packet(5)
            packet.write_bool(click)
            packet.write_string(key)
            packet.compress()
            send_msg(self.sobj, packet.buffer)

        def click_detection(netid):
            packet = Packet(6)
            packet.write_uint32(netid)
            packet.compress()
            send_msg(self.sobj, packet.buffer)

        def heartbeat():
            packet = Packet(7)
            packet.compress()
            send_msg(self.sobj, packet.buffer)

        def disconnect():
            packet = Packet(254)
            packet.compress()
            send_msg(self.sobj, packet.buffer)

        return Properties({
            "chat": chat,
            "command": command,
            "move": move,
            "player_input": player_input,
            "click_detection": click_detection,
            "heartbeat": heartbeat,
            "disconnect": disconnect
        })
