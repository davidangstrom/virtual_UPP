from spritesheet import Spritesheet
import pygame
#1: rak vägg upp	        (16,0,16,16)
#2: vägg kant uppåt vänster (0,0,16,16)
#3: vägg kant uppåt höger   (32,0,16,16)
#4: vänster vägg            (0,16,16,16)
#5: vägg kant nedåt vänster (0,32,16,16)
#6: golv                    (0,48,16,16)
#7: rak vägg ned            (16,32,16,16)
#8: vägg kant nedåt höger   (32,32,16,16)
#9: höger vägg              (32,16,16,16)

SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 800

map_tiles = []
with open("resources/map_sprites/map.txt") as f:
    map_tiles = [line[:-1] for line in f]
    map_tiles = [int(item) for sublist in map_tiles for item in sublist]

#print(len(map_tiles))
map_sprites = Spritesheet("resources/map_sprites/TheLostDungeonGrey.png")
sprite_1 = map_sprites.get_sprite(16,0,16,16)
sprite_2 = map_sprites.get_sprite(0,0,16,16)
sprite_3 = map_sprites.get_sprite(32,0,16,16)
sprite_4 = map_sprites.get_sprite(0,16,16,16)
sprite_5 = map_sprites.get_sprite(0,32,16,16)
sprite_6 = map_sprites.get_sprite(0,48,16,16)
sprite_7 = map_sprites.get_sprite(16,32,16,16)
sprite_8 = map_sprites.get_sprite(32,32,16,16)
sprite_9 = map_sprites.get_sprite(32,16,16,16)

class Map:
    def __init__(self):
        self.x = 0

    def draw(self, win):
        win.blit(self.map, (self.x,self.y) )

    def draw_map(self, win):
        #win.blit(sprite_1, (1000,1000))
        
        counter = 0
        for y in range(0, SCREEN_HEIGHT, 16):
            for x in range(0, SCREEN_WIDTH, 16):
                if(map_tiles[counter] == 1):
                    win.blit(sprite_1, (x, y))
                if(map_tiles[counter] == 2):
                    win.blit(sprite_2, (x, y))
                if(map_tiles[counter] == 3):
                    win.blit(sprite_3, (x, y))
                if(map_tiles[counter] == 4):
                    win.blit(sprite_4, (x, y))
                if(map_tiles[counter] == 5):
                    win.blit(sprite_5, (x, y))
                if(map_tiles[counter] == 6):
                    win.blit(sprite_6, (x, y))
                if(map_tiles[counter] == 7):
                    win.blit(sprite_7, (x, y))
                if(map_tiles[counter] == 8):
                    win.blit(sprite_8, (x, y))
                if(map_tiles[counter] == 9):
                    win.blit(sprite_9, (x, y))
                counter+=1
                #print(counter)