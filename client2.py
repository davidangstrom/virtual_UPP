import pygame
import sys
import socket
import select
import pickle
import pyaudio
import threading
from Network import Network
#from player import Player
from _thread import *
from spritesheet import Spritesheet
from map import Map

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BUFFERSIZE = 2048 * 3
S_BUFF = 2048

audio_format = pyaudio.paInt16
channels = 1
rate = 20000

pygame.init()
canvas = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('chat room') 
#win.fill((0,0,0))

"""
PLAYER STUFF
"""

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)


player_sprites = Spritesheet("resources/player_sprites/1.png")
player_down = [
    player_sprites.get_sprite(0, 0, 48, 64),
    player_sprites.get_sprite(48, 0, 48, 64),
    player_sprites.get_sprite(96, 0, 48, 64),
    player_sprites.get_sprite(144, 0, 48, 64)
]

player_left = [
    player_sprites.get_sprite(0, 64, 48, 64),
    player_sprites.get_sprite(48, 64, 48, 64),
    player_sprites.get_sprite(96, 64, 48, 64),
    player_sprites.get_sprite(144, 64, 48, 64),
]

player_right = [
    player_sprites.get_sprite(0, 128, 48, 64),
    player_sprites.get_sprite(48, 128, 48, 64),
    player_sprites.get_sprite(96, 128, 48, 64),
    player_sprites.get_sprite(144, 128, 48, 64),
]

player_up = [
    player_sprites.get_sprite(0, 192, 48, 64),
    player_sprites.get_sprite(48, 192, 48, 64),
    player_sprites.get_sprite(96, 192, 48, 64),
    player_sprites.get_sprite(144, 192, 48, 64),
]


class Player():
    def __init__(self, x, y, id):
        self.x = x
        self.y = y
        self.height = 48
        self.width = 64
        self.rect = (x,y, self.width, self.height)
        self.id = id
        self.vel = 50
        self.current_move = 0
        self.last_move = 0 #0 = down, 1 = left, 2 = right, 3 = up
        self.move_counter = 0
        self.idle = True
     


    def update(self, win, pressed_keys = []):
        if pressed_keys[K_UP] or pressed_keys[K_DOWN] or pressed_keys[K_LEFT] or pressed_keys[K_RIGHT]:
            self.idle = False
            if pressed_keys[K_UP]:
                self.y -= 3
                self.current_move = 3
            if pressed_keys[K_DOWN]:
                self.y += 3
                self.current_move = 0
            if pressed_keys[K_LEFT]:
                self.x -= 3
                self.current_move = 1
            if pressed_keys[K_RIGHT]:
                self.x += 3
                self.current_move = 2
        else:
            self.idle = True

        if self.y <= 0:
            self.y += 3
        if self.y >= SCREEN_HEIGHT - self.height:
            self.y -= 3
        if self.x <= 0:
            self.x += 3
        if self.x >= SCREEN_WIDTH - self.width:
            self.x -= 3
        
        self.rect =(self.x, self.y, 20, 20)
        self.render(win)

    def render(self, win):
        if self.current_move != self.last_move:
            self.move_counter = 0

        if self.current_move == 0:
            win.blit(player_down[self.move_counter], (self.x, self.y))
            self.last_move = 0
        elif self.current_move == 1:
            win.blit(player_left[self.move_counter], (self.x, self.y))
            self.last_move = 1
        elif self.current_move == 2:
            win.blit(player_right[self.move_counter], (self.x, self.y))
            self.last_move = 2
        else:
            win.blit(player_up[self.move_counter], (self.x, self.y))
            self.last_move = 3


        if self.idle != True:
            if self.move_counter == 3:
                self.move_counter = 0
            self.move_counter += 1
        pygame.display.update()


"""
PLAYER STUFF
"""


#ss = spritesheet("resources/pepe.png")
#image = pygame.image.load("resources/pepe.png").convert()
#image = pygame.transform.scale(image, (int(image.get_width() * 0.25), int(image.get_height() * 0.25)))

#win.blit(image, [200,200])

"""
clock = pygame.time.Clock()
while True: 
    for sprite in player_down:
        clock.tick(10)
        canvas.fill((255, 255, 255))
        canvas.blit(sprite, (0, SCREEN_HEIGHT - 400))
        win.blit(canvas, (0,0))
        pygame.display.update()
"""
def draw_and_receive(win, main_p, map, v_stream, ge, n, pressed):
    #win.fill((0,0,0))
    #print_lock.acquire()
    map.draw(win)
    main_p.update(win, pressed)  
    try:
        reply = n.send(ge)
        if reply:
            all_players = reply[0]
            for p in all_players.values():
                if p.id != main_p.id:
                    p.render(win)
                    pygame.display.update()

            for v in reply[1]:
                v_stream.write(v)
        else:
            map.draw(win)
            main_p.update(pressed, win)
            pygame.display.update()

    except Exception as e:
        print("is MARK here", e) #oh hi mark, sometimes spits out invalid load key, not sure why.
        pass

def main():
    run = True
    n = Network()
    player_tup = n.connect()
    main_player = Player(player_tup.x, player_tup.y, player_tup.id)
    map = Map()
    map.draw(win)

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
        draw_and_receive(win, main_player, map, playing_stream, ge, n, pressed_keys)
        #pygame.display.update()

main()