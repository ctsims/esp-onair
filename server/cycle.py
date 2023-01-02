#quick script to test the sign by broadcasting a signal to the multicast group which will flip on/off

import socket
import _thread
import importlib
from uuid import getnode

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.connect(("8.8.8.8", 80))
ip_local = sock.getsockname()[0]
#ip_local = "127.0.0.1"
sock.close()


MCAST_GRP = '239.0.82.66'
MCAST_PORT = 9816
MESSAGE = b"{signal: 2}"

MULTICAST_TTL = 5

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, MULTICAST_TTL)

sock.bind((ip_local, MCAST_PORT))

sock.sendto(MESSAGE, (MCAST_GRP, MCAST_PORT))

