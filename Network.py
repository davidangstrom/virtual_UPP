import pygame
import sys
import socket
import select
import pickle
import pyaudio

import time

BUFFERSIZE = 2048 * 3

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.setblocking(1)
        #self.client.settimeout()
        self.server = "92.35.28.148"
        self.port = 5555
        self.addr = (self.server, self.port)
        #self.player = self.connect()
        #self.pos = self.get_pos()
        #print(self.id)

    def connect(self):
        self.client.setblocking(1) #Needs to block to get connection information (starting position)
        while True:
            try:
                self.client.connect(self.addr)
                return pickle.loads(self.client.recv(BUFFERSIZE))
            except:
                print(sys.exc_info()[0:1])
                print("maybe here0")
                pass
    
    def send(self, data):
        self.client.setblocking(0) #Data may or may not have been sent from server, cases are handled in client.
        try:
            self.client.send(pickle.dumps(data))
            temp = self.client.recv(BUFFERSIZE)
            return pickle.loads(temp)
        except socket.error as e:
            print("here", e)
            return None