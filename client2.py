import pygame
import sys
import socket
import select
import pickle
import pyaudio
from Network import Network
from player import Player

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

def redraw_window(win, main_player):
    #win.fill((0,0,0))
    main_player.render(win)
    #pygame.display.update()

def main():
    run = True
    n = Network()
    #start_pos = n.connect()
    main_player = n.connect()# Player(start_pos[0], start_pos[1], 0)

    print(main_player.x)
    clock = pygame.time.Clock()

    other_players = []

    p = pyaudio.PyAudio()
    playing_stream = p.open(format=audio_format, channels=channels,\
        rate=rate, output=True, frames_per_buffer=S_BUFF)
    recording_stream = p.open(format=audio_format, channels=channels,\
        rate=rate, input=True, frames_per_buffer=S_BUFF)

    while run:
        clock.tick(5000)

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
        reply = n.send(ge)

        win.fill((0,0,0))
        for p in reply[0].values():
            redraw_window(win, main_player)
            if p.id != main_player.id:
                playing_stream.write(reply[1])
                p.render(win)
                print(p.x)
        pygame.display.update()
        #playing_stream.write(reply[1])

main()