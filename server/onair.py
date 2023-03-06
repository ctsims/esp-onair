#Run with pythonw on startup for headless

from wcdetect import WebcamDetect

import socket
import _thread
import importlib
import time
import requests
from uuid import getnode

EVENT_ON=None
EVENT_OFF=None
try:
    from secrets import *
except:
    print("Couldn't find secrets.py, webhook support unavailable")
    WEBHOOK_BASE=None


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

def webhook_on():
    if not EVENT_ON:
        return
    ifttt_webhook(EVENT_ON)

def webhook_off():
    if not EVENT_OFF:
        return
    ifttt_webhook(EVENT_OFF)

def ifttt_webhook(event_id):
    if not WEBHOOK_BASE:
        return

    r = requests.get(WEBHOOK_BASE % event_id)

while True:
    time.sleep(1)
    read_status = wc.isActive()

    if read_status != current_status:
        if read_status:
            print("On Air")
            send(MESSAGE_ON)
            webhook_on()
        else:
            print("Off Air")
            send(MESSAGE_OFF)
            webhook_off()

    current_status = read_status

