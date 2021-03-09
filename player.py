from spritesheet import Spritesheet
from globals import *
import pygame

player_down = {}
player_left = {}
player_right = {}
player_up = {}

def helper_helper(dict, key, value):
        if key not in dict:
            dict[key] = []
        dict[key].append(value)

class Player():
    def __init__(self, x, y, id, chosen_sprite):
        #Positions
        self.x = x
        self.y = y
        self.height = 48
        self.width = 64
        self.rect = (x,y, self.width, self.height)
        self.id = id

        #Movement
        self.vel = 7
        self.current_move = 0
        self.last_move = 0 #0 = down, 1 = left, 2 = right, 3 = up
        self.move_counter = 0
        self.idle = True

        self.chosen_sprite = chosen_sprite

        #voice chat
        #self.muted = False

    def load_helper(self):
        global player_down 
        global player_left
        global player_right
        global player_up

        for char in range(1, 26):
            player_sprites = Spritesheet("resources/player_sprites/{}.png".format(char))
            for direction in range(0,4):
                if char == 4: #Special one
                    if direction == 0:
                        helper_helper(player_down, char, [
                            player_sprites.get_sprite(0, 0, 64, 64),
                            player_sprites.get_sprite(64, 0, 64, 64),
                            player_sprites.get_sprite(128, 0, 64, 64),
                            player_sprites.get_sprite(192, 0, 64, 64)
                    ])
                    elif direction == 1:
                        helper_helper(player_left, char , [
                            player_sprites.get_sprite(0, 64, 64, 64),
                            player_sprites.get_sprite(64, 64, 64, 64),
                            player_sprites.get_sprite(128, 64, 64, 64),
                            player_sprites.get_sprite(192, 64, 64, 64),
                    ])
                    elif direction == 2:
                        helper_helper(player_right, char, [
                            player_sprites.get_sprite(0, 128, 64, 64),
                            player_sprites.get_sprite(64, 128, 64, 64),
                            player_sprites.get_sprite(128, 128, 64, 64),
                            player_sprites.get_sprite(192, 128, 64, 64),
                    ])
                    else:
                        helper_helper(player_up, char, [
                            player_sprites.get_sprite(0, 192, 64, 64),
                            player_sprites.get_sprite(64, 192, 64, 64),
                            player_sprites.get_sprite(128, 192, 64, 64),
                            player_sprites.get_sprite(192, 192, 64, 64),
                    ])
                else:
                    if direction == 0:
                        helper_helper(player_down, char, [
                            player_sprites.get_sprite(0, 0, 48, 64),
                            player_sprites.get_sprite(48, 0, 48, 64),
                            player_sprites.get_sprite(96, 0, 48, 64),
                            player_sprites.get_sprite(144, 0, 48, 64)
                        ])
                    elif direction == 1:
                        helper_helper(player_left, char, [
                            player_sprites.get_sprite(0, 64, 48, 64),
                            player_sprites.get_sprite(48, 64, 48, 64),
                            player_sprites.get_sprite(96, 64, 48, 64),
                            player_sprites.get_sprite(144, 64, 48, 64),
                        ])
                    elif direction == 2:
                        helper_helper(player_right, char, [
                            player_sprites.get_sprite(0, 128, 48, 64),
                            player_sprites.get_sprite(48, 128, 48, 64),
                            player_sprites.get_sprite(96, 128, 48, 64),
                            player_sprites.get_sprite(144, 128, 48, 64),
                        ])
                    else:
                        helper_helper(player_up, char, [
                            player_sprites.get_sprite(0, 192, 48, 64),
                            player_sprites.get_sprite(48, 192, 48, 64),
                            player_sprites.get_sprite(96, 192, 48, 64),
                            player_sprites.get_sprite(144, 192, 48, 64),
                        ])

    def load_images(self):
        #print("resources/player_sprites/{}.png".format(self.chosen_sprite))
        player_sprites = Spritesheet("resources/player_sprites/{}.png".format(self.chosen_sprite))
        global player_down
        global player_left
        global player_right
        global player_up
        if self.chosen_sprite == 4: #The wierd one
            player_down = [
            player_sprites.get_sprite(0, 0, 64, 64),
            player_sprites.get_sprite(64, 0, 64, 64),
            player_sprites.get_sprite(128, 0, 64, 64),
            player_sprites.get_sprite(192, 0, 64, 64)
            ]

            player_left = [
                player_sprites.get_sprite(0, 64, 64, 64),
                player_sprites.get_sprite(64, 64, 64, 64),
                player_sprites.get_sprite(128, 64, 64, 64),
                player_sprites.get_sprite(192, 64, 64, 64),
            ]

            player_right = [
                player_sprites.get_sprite(0, 128, 64, 64),
                player_sprites.get_sprite(64, 128, 64, 64),
                player_sprites.get_sprite(128, 128, 64, 64),
                player_sprites.get_sprite(192, 128, 64, 64),
            ]

            player_up = [
                player_sprites.get_sprite(0, 192, 64, 64),
                player_sprites.get_sprite(64, 192, 64, 64),
                player_sprites.get_sprite(128, 192, 64, 64),
                player_sprites.get_sprite(192, 192, 64, 64),
            ]

        else:
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

    def update(self, win, pressed_keys):
        if pressed_keys[K_UP] or pressed_keys[K_DOWN] or pressed_keys[K_LEFT] or pressed_keys[K_RIGHT] or pressed_keys[K_m]:
            self.idle = False
            if pressed_keys[K_UP]:
                self.y -= self.vel
                self.current_move = 3
            if pressed_keys[K_DOWN]:
                self.y += self.vel
                self.current_move = 0
            if pressed_keys[K_LEFT]:
                self.x -= self.vel
                self.current_move = 1
            if pressed_keys[K_RIGHT]:
                self.x += self.vel
                self.current_move = 2
            #if pressed_keys[K_m]:
            #   self.muted = not self.muted
            #   return None
        else:
            self.idle = True

        if self.y <= 0:
            self.y += self.vel
        if self.y >= SCREEN_HEIGHT - self.height - 25:
            self.y -= self.vel
        if self.x <= 0:
            self.x += self.vel
        if self.x >= SCREEN_WIDTH - self.width:
            self.x -= self.vel
        
        self.rect = (self.x, self.y, 20, 20)
        self.render(win)

    def render(self, win):
        if self.current_move != self.last_move:
            self.move_counter = 0
    
        if self.current_move == 0:
            win.blit(player_down[self.chosen_sprite][0][self.move_counter], (self.x, self.y))
            self.last_move = 0
        elif self.current_move == 1:
            win.blit(player_left[self.chosen_sprite][0][self.move_counter], (self.x, self.y))
            self.last_move = 1
        elif self.current_move == 2:
            win.blit(player_right[self.chosen_sprite][0][self.move_counter], (self.x, self.y))
            self.last_move = 2
        else:
            win.blit(player_up[self.chosen_sprite][0][self.move_counter], (self.x, self.y))
            self.last_move = 3


        if self.idle != True:
            if self.move_counter == 3:
                self.move_counter = 0
            self.move_counter += 1
        #pygame.display.update()