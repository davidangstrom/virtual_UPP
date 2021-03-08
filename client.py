import pygame
import sys
import socket
import select
import pickle
import pyaudio
import threading
from array import array
from Network import Network
from _thread import *
from spritesheet import Spritesheet

SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 800
BUFFERSIZE = 8192
#BUFFERSIZE = 8400


S_BUFF = 2048
audio_format = pyaudio.paInt16
channels = 1
rate = 44100
silence = chr(0)*S_BUFF*channels*2 
THRESHOLD = 100

pygame.init()
canvas = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('chat room') 

from map import Map
from player import Player #These had to be imported after pygame.display for converting images

def draw_and_receive(win, main_p, map, v_stream, ge, n, pressed, all_p):
    map.draw_map(win)
    main_p.update(win, pressed) 

    try:
        reply = n.send(ge)
        if reply != None:
            all_p = reply[0]
            for loc_p in all_p:
                if loc_p not in reply[0]:
                    del all_p[loc_p]
            for p in all_p.values():
                if p.id != main_p.id:
                    p.render(win)
                    pygame.display.update()

            for v in reply[1]:
                """
                #little endian
                snd_data = array('h', v)
                if sys.byteorder == "big":
                    snd_data.byteswap()
                
                if max(snd_data) < THRESHOLD:
                    v_stream.write(silence)
                else:
                    v_stream.write(v)
                """
                if v == '':
                    v_stream.write(silence)
                    print(v_stream.get_write_available())
                else:
                    v_stream.write(v)
                
        else:
            map.draw_map(win)
            main_p.update(win, pressed)
            pygame.display.update()

    except Exception as e:
        print("is MARK here", e) #oh hi mark, sometimes spits out invalid load key, not sure why.
        pass

def main():
    run = True
    n = Network()
    player_tup = n.connect()
    main_player = Player(player_tup.x, player_tup.y, player_tup.id)
    main_player.load_images()
    map = Map()
    map.draw_map(win)
    pygame.display.update()
    clock = pygame.time.Clock()

    p = pyaudio.PyAudio()
    playing_stream = p.open(format=audio_format, channels=channels,\
        rate=rate, output=True, frames_per_buffer=S_BUFF)
    recording_stream = p.open(format=audio_format, channels=channels,\
        rate=rate, input=True, frames_per_buffer=S_BUFF)

    all_players = {}
    while run:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()

        #main_player.render(win)

        voice = recording_stream.read(S_BUFF)
        pressed_keys = pygame.key.get_pressed()
        ge = ['position update', main_player, voice]
        
        #start_new_thread(draw_and_receive, (win, main_player, playing_stream, ge, n))
        draw_and_receive(win, main_player, map, playing_stream, ge, n, pressed_keys, all_players)
        #pygame.display.update()


main()