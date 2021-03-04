import pygame
import sys
import socket
import select
import pickle
import pyaudio


BUFFERSIZE = 2048 * 3

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.setblocking(1)
        self.client.settimeout(0.05)
        self.server = "192.168.10.148"
        self.port = 5555
        self.addr = (self.server, self.port)
        #self.player = self.connect()
        #self.pos = self.get_pos()
        #print(self.id)

    def connect(self):
        try:
            self.client.connect(self.addr)
            return pickle.loads(self.client.recv(BUFFERSIZE))
        except:
            print(sys.exc_info()[0:1])
            pass
    
    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            data = []
            while True:
                try:
                    rec = self.client.recv(BUFFERSIZE)
                    if not rec: break
                    data.append(rec)
                except Exception as e:
                    print(e)
                    break
            
            return pickle.loads(b"".join(data))
            #return pickle.loads(self.client.recv(BUFFERSIZE))
        except socket.error as e:
            print(e)
        


    #def get_pos(self):
    #    return self.pos
