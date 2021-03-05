import socket
import asyncore
import select
import random
import pickle
import time
import sys
from _thread import *
from player import Player
import threading


BUFFERSIZE = 2048 * 3
START_POS = (100,100)

server = "192.168.10.148"
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

def threaded_client(conn, current_player):
    new_player = Player(START_POS[0], START_POS[1], current_player)
    conn.send(pickle.dumps(new_player))
    players[current_player] = new_player
    conn.setblocking(1)
    reply = ""
    while True:
        try:
            #rec = conn.recv(BUFFERSIZE)
            data = pickle.loads(conn.recv(BUFFERSIZE))
            #reply = data.decode("utf-8")
            if not data:
                print("Disconnected")
                break
            
            players[current_player].x = data[1]
            players[current_player].y = data[2]
            players[current_player].rect = (data[1], data[2], 20, 20)
            #print ("x: ", data[1], " y: ", data[2])
            #[1] = x
            #[2] = y
            #[3] = voice stream
            conn.send(pickle.dumps([players, data[3]])) #How does this wörk??
        except Exception as e:
            print(e)
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
