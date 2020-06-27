import socket
import struct
import sys

assert float(sys.version[:3]) >= 3.7

def kickoff(side='Left'):
    '''side = Left or Right'''
    msg = f'(playMode KickOff_{side})'
    L = len(msg)
    bm = struct.pack(f'!i{L}s', L, msg.encode())
    print('send', bm)
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect(('localhost', 3200))
    s.send(bm)
#    r = s.recv(2048)
    s.close()


def kickoff_penalty(side='Left'):
    pass

if __name__ == '__main__':
    kickoff('Left')
