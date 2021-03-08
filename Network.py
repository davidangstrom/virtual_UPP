import pygame
import sys
import socket
import select
import pickle
import pyaudio
import struct

import time

BUFFERSIZE = 8192

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.setblocking(1)
        #self.client.settimeout()
        self.server = "92.35.28.148"
        #self.server = "192.168.10.148"
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
            except Exception as e:
                print("maybe here ", e)
                pass
    
    def send(self, data):
        self.client.setblocking(0) #Data may or may not have been sent from server, cases are handled in client.
        data = pickle.dumps(data)
        try:
            print(sys.getsizeof(data))
            self.client.send(data)
            temp = self.client.recv(BUFFERSIZE)
            return pickle.loads(temp)
        except socket.error as e:
            print("here", e)
            return None