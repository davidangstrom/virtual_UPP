import socket
import asyncore
import select
import random
import pickle
import time
import sys
from _thread import *
import threading
#from player import Player


class Player():
    def __init__(self, x, y, id):
        self.x = x
        self.y = y
        self.height = 48
        self.width = 64
        self.rect = (x,y, self.width, self.height)
        self.id = id
        self.vel = 7
        self.current_move = 0
        self.last_move = 0 #0 = down, 1 = left, 2 = right, 3 = up
        self.move_counter = 0
        self.idle = True

BUFFERSIZE = 8192
START_POS = (100,100)

#server = "192.168.10.148"
#server = "92.35.28.148"
server = "0.0.0.0"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)


s.listen()
print("waiting for connection")



players = {}
connections = {}

voice = {}
prev_sent_voice = {}

def threaded_client(conn, current_player):
    new_player = Player(START_POS[0], START_POS[1], current_player)
    conn.send(pickle.dumps(new_player))
    players[current_player] = new_player
    conn.setblocking(1)
    reply = ""
    while True:
        try:
            rec = conn.recv(BUFFERSIZE)
            print(sys.getsizeof(rec))
            data = pickle.loads(rec)
            voice[current_player] = data[2]

            #reply = data.decode("utf-8")
            if not data:
                print("Disconnected")
                break

            players[current_player] = data[1]

            #print ("x: ", data[1], " y: ", data[2])
            #[1] = message, currently not needed.
            #[2] = Player.
            #[3] = voice stream.
            send_v = []
            for v in voice:
                if v != current_player:
                    if v in prev_sent_voice:
                        if voice[v] != prev_sent_voice[v]:
                            send_v.append(voice[v])
                            prev_sent_voice[v] = voice[v]
                    else:
                        send_v.append(voice[v])
                        prev_sent_voice[v] = voice[v]
                    
            conn.send(pickle.dumps([players, send_v]))
        except Exception as e:
            print("maybe here", e)
            break

    print("Lost connection")
    del connections[current_player]
    del players[current_player]
    conn.close()


current_player = 0
while True:
    conn, addr = s.accept()
    connections[current_player] = conn
    print("Connected to", addr)

    start_new_thread(threaded_client, (conn, current_player))
    current_player += 1
