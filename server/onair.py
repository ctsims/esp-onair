#Run with pythonw on startup for headless

from wcdetect import WebcamDetect

import socket
import _thread
import importlib
import time
from uuid import getnode

#Identify the right networking interface. 
#NOTE: This makes a network request to figure out which interface is the right one. If you run a VPN this will likely find the VPN interface rather than your local network
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.connect(("8.8.8.8", 80))
ip_local = sock.getsockname()[0]
sock.close()


MCAST_GRP = '239.0.82.66'
MCAST_PORT = 9816

MESSAGE_ON = b"{signal: 1}"
MESSAGE_OFF = b"{signal: 0}"

MULTICAST_TTL = 5

wc = WebcamDetect()

current_status = False;

def send(msg):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, MULTICAST_TTL)

    sock.bind((ip_local, MCAST_PORT))

    sock.sendto(msg, (MCAST_GRP, MCAST_PORT))
    sock.close()

while True:
    time.sleep(1)
    read_status = wc.isActive()

    if read_status != current_status:
        if read_status:
            print("On Air")
            send(MESSAGE_ON)
        else:
            print("Off Air")
            send(MESSAGE_OFF)

    current_status = read_status

