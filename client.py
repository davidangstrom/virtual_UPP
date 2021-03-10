import pygame
import sys
import socket
import select
import pickle
import pyaudio
import threading
import wave
from globals import *
from array import array
from Network import Network
from _thread import *
from spritesheet import Spritesheet

pygame.init()
canvas = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('chat room') 

def background_music(filename, menu):
    p_music = pyaudio.PyAudio()
    background = wave.open(filename, 'rb')
    music_playing_stream = p_music.open(rate = background.getframerate(),
    channels = background.getnchannels(),
    format = p_music.get_format_from_width(background.getsampwidth()),
    output = True,
    frames_per_buffer = 1024)
    background = wave.open(filename)
    data = background.readframes(S_BUFF)
    while not menu.char_selected:
        music_playing_stream.write(data)
        data = background.readframes(S_BUFF)
        if data == b'':
            background.rewind()
            data = background.readframes(S_BUFF)

from menu import Menu
m = Menu()
start_new_thread(background_music, ("resources/music/hissmusik1.wav", m))
while not m.done:
    m.draw_menu(win)
    pressed_keys = pygame.key.get_pressed()
    m.update_menu(pressed_keys)


    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

if m.sel == 1:
    pygame.quit()
    sys.exit()
pygame.event.clear()
#pygame.key.set_repeat(1, 25)

char_clock = pygame.time.Clock()
chosen_char = 0
while not m.char_selected:
    wait = True
    win.fill((0,0,0))
    while wait:
        char_clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            m.display_characters(win)
            pressed_keys = pygame.key.get_pressed()
            chosen_char = m.update_character_sel(pressed_keys)
            wait = False


from map import Map
from player import Player #These had to be imported after pygame.display for converting images

def gensin(frequency, duration, sampRate):
    
    """ Frequency in Hz, duration in seconds and sampleRate
        in Hz"""

    cycles = np.linspace(0,duration*2*np.pi,num=duration*sampRate)
    wave = np.sin(cycles*frequency,dtype='float32')
    t = np.divide(cycles,2*np.pi)


def draw_and_receive(win, main_p, map, v_stream, ge, n, pressed, all_p):
    map.draw_map(win)
    main_p.update(win, pressed) 
    reply = n.send(ge)
    if reply != None:
        all_p = reply[0]
        for p in all_p.values():
            if p.id != main_p.id:
                p.render(win)
        pygame.display.update()

        for v in reply[1]:
            #little endian
            snd_data = array('h', v)
            if sys.byteorder == "big":
                snd_data.byteswap()
            
            if max(snd_data) < THRESHOLD:
                v_stream.write(silence)
            else:
                v_stream.write(v)
    else:
        for p in all_p:
            p.render(win)
        map.draw_map(win)
        main_p.update(win, pressed)
        pygame.display.update()

    #except Exception as e:
    #    print("is MARK here", e) #oh hi mark, sometimes spits out invalid load key, not sure why.
    #    pass                     #Nowadays seems to spit out 0 for for some reason.


def main():
    n = Network()
    player_tup = n.connect()
    main_player = Player(player_tup.x, player_tup.y, player_tup.id, chosen_char)
    main_player.load_helper()

    print("sending data")
    n.send(chosen_char) #have to tell server which chosen char for first iteration.
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
    run = True
    while run:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        #main_player.render(win)

        voice = recording_stream.read(S_BUFF)
        pressed_keys = pygame.key.get_pressed()
        ge = ['position update', main_player, voice]
        
        #start_new_thread(draw_and_receive, (win, main_player, playing_stream, ge, n))
        draw_and_receive(win, main_player, map, playing_stream, ge, n, pressed_keys, all_players)
        #pygame.display.update()


main()
pygame.quit()
sys.exit()