import pyaudio
import pygame

SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 800
BUFFERSIZE = 8192

S_BUFF = 256 * 6
rate = 44100
#audio_format = pyaudio.paInt16
audio_format = pyaudio.paInt16
channels = 1

#rate = 10000
silence = chr(0)*S_BUFF*channels*1
THRESHOLD = 100

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    K_RETURN,
    K_KP_ENTER,
    K_m
)
