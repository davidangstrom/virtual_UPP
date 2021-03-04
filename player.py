import pygame
import pyaudio

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BUFFERSIZE = 2048 * 3
S_BUFF = 2048

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

#main_char = pygame.image.load('temp_char.png')#.convert()
class Player():
    def __init__(self, x, y, id):
        self.x = x
        self.y = y
        self.rect = (x,y, 20, 20)
        self.id = id


    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.y -= 5
        if pressed_keys[K_DOWN]:
            self.y += 5
        if pressed_keys[K_LEFT]:
            self.x -= 5
        if pressed_keys[K_RIGHT]:
            self.x += 5

        self.rect =(self.x, self.y, 20, 20)

    def render(self, win):
        pygame.draw.rect(win, (255,255,255), self.rect)
        #print(self.rect.x + self.rect.y)