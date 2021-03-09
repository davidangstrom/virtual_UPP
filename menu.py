import pygame
from globals import *
from spritesheet import Spritesheet

player_sprites = {}
for i in range(1,26):
    player_sprites[i] = Spritesheet("resources/player_sprites/{}.png".format(i)).get_sprite(0, 0, 48, 64)

class Menu:
    def __init__(self):
        self.sel = 0 #0: play, 1: exit
        self.font = pygame.font.SysFont('Comic Sans MS', 60)
        self.color_sel = (255,0,0)
        self.color_non_sel = (100,100,100)
        self.done = False

        self.sel_char = 1
        self.char_selected = False

    def draw_menu(self, win):
        if self.sel == 0:
            text_play = self.font.render('play', False, self.color_sel)
            text_exit = self.font.render('exit', False, self.color_non_sel)
        else:
            text_play = self.font.render('play', False, self.color_non_sel)
            text_exit = self.font.render('exit', False, self.color_sel)

        text_play_rect = text_play.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/3))
        text_exit_rect = text_exit.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/3*2))

        win.blit(text_play, text_play_rect)
        win.blit(text_exit, text_exit_rect)
        pygame.display.update()

    def update_menu(self, pressed_keys):
        if pressed_keys[K_UP]:
            if self.sel == 1:
                self.sel = 0 #from exit to play
        if pressed_keys[K_DOWN]:
            if self.sel == 0:
                self.sel = 1 #from play to exit
        if pressed_keys[K_RETURN]:
            self.done = True

    def display_characters(self, win):
        for i, character in enumerate(player_sprites.values()):
            if i != self.sel_char:
                win.blit(character, (i*64, SCREEN_HEIGHT/2))
            else:
                pygame.draw.rect(win, (255,0,0), (i*64 - 1, SCREEN_HEIGHT/2 + 1, 50, 66))
                win.blit(character, (i*64, SCREEN_HEIGHT/2))
        pygame.display.update()


    def update_character_sel(self, pressed_keys):
        if pressed_keys[K_LEFT]:
            if self.sel_char != 0:
                self.sel_char -= 1
        if pressed_keys[K_RIGHT]:
            if self.sel_char != 24:
                self.sel_char += 1
        if pressed_keys[K_RETURN]:
                self.char_selected = True
        return self.sel_char+1