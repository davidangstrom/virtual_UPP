import socket
import asyncore
import select
import random
import pickle
import time
import sys
from _thread import *
import threading
from player import Player
from globals import *

START_POS = (100,100)

#server = "192.168.10.148"
#server = "92.35.28.148"
server = "0.0.0.0"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    print(e)


s.listen()
print("waiting for connection")



players = {}
connections = {}

voice = {}
prev_sent_voice = {}

def threaded_client(conn, current_player):
    conn.send(pickle.dumps(Player(START_POS[0], START_POS[1], current_player, 0))) #Connection accepted, send starting pos
    try:
        rec = conn.recv(BUFFERSIZE) #Wait for first send which is the selected char
    except Exception as e:
        print(e)
        del connections[current_player]
        conn.close()
        return None

    else:
        chosen_char = pickle.loads(rec)
        new_player = Player(START_POS[0], START_POS[1], current_player, chosen_char) #append this to players

    players[current_player] = new_player
    conn.setblocking(1)
    #conn.setblocking(0)
    reply = ""
    while True:
        try:
            rec = conn.recv(BUFFERSIZE)
        
            data = pickle.loads(rec)
            voice[current_player] = data[2]

            #reply = data.decode("utf-8")
            if not data:
                print("Disconnected")
                break

            players[current_player] = data[1]

            #[0] = message, currently not used
            #[1] = player
            #[2] = voice
            send_v = []
            for v in voice:
                if v != current_player:
                    if v in prev_sent_voice:
                        if voice[v] != prev_sent_voice[v]: #or not players[v].muted:
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
