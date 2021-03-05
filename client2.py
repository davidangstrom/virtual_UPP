import pygame
import sys
import socket
import select
import pickle
import pyaudio
import threading
from Network import Network
from player import Player
from _thread import *

import pygame
import sys
import socket
import select
import pickle
import pyaudio

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BUFFERSIZE = 2048 * 3
S_BUFF = 2048

audio_format = pyaudio.paInt16
channels = 1
rate = 20000

pygame.init()
win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
win.fill((0,0,0))

print_lock = threading.Lock()

def draw_and_receive(win, main_p, v_stream, ge, n):
    win.fill((0,0,0))
    #print_lock.acquire()
    try:
        reply = n.send(ge)
        if reply:
            for p in reply[0].values():      
                if p.id != main_p.id:
                    p.render(win)
            v_stream.write(reply[1])
        #print_lock.release()
    except Exception as e:
        print("is MARK here", e) #oh hi mark
        #print_lock.release()
        pass

def main():
    run = True
    n = Network()
    #start_pos = n.connect()
    main_player = n.connect()# Player(start_pos[0], start_pos[1], 0)

    clock = pygame.time.Clock()

    other_players = []

    p = pyaudio.PyAudio()
    playing_stream = p.open(format=audio_format, channels=channels,\
        rate=rate, output=True, frames_per_buffer=S_BUFF)
    recording_stream = p.open(format=audio_format, channels=channels,\
        rate=rate, input=True, frames_per_buffer=S_BUFF)
    while run:
        clock.tick(144)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()

        pressed_keys = pygame.key.get_pressed()


        main_player.update(pressed_keys)
        #main_player.render(win)

        voice = recording_stream.read(S_BUFF)
        ge = ['position update', main_player.x, main_player.y, voice]

        #print("size of voice stream", sys.getsizeof(voice))
        #start_new_thread(draw_and_receive, (win, main_player, playing_stream, ge, n))
        draw_and_receive(win, main_player, playing_stream, ge, n)

        main_player.render(win)
        pygame.display.update()
        #playing_stream.write(reply[1])

main()