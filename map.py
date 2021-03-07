import pygame
class Map:
    def __init__(self):
        self.map = pygame.image.load("resources/eggs1.png")
        self.x = 0
        self.y = 0

    def draw(self, win):
        win.blit(self.map, (self.x,self.y) )
        