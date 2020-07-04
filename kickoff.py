import socket
import struct
import sys
from logger3d import I, L


def kickoff(side='Left',host='localhost'):
    '''side = Left or Right'''
    msg = f'(playMode KickOff_{side})'
    L = len(msg)
    bm = struct.pack(f'!i{L}s', L, msg.encode())
    I(f'send {bm}')
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((host, 3200))
    s.send(bm)
#    r = s.recv(2048)
    s.close()


def kickoff_penalty(side='Left'):
    pass

if __name__ == '__main__':
    kickoff('Left')
