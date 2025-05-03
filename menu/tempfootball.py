#when done with game logic immplement this into the main football.py file

import pygame
import sys
from menu import *

class game():
    def __init__(self):
        pygame.init()
        self.running, self.playing = True, False #running and playing state
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False #key states
        self.DISPLAY_W, self.DISPLAY_H = 1280, 720 #canvas size
        self.display = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H)) #creates a canvas
        self.window = pygame.display.set_mode((self.DISPLAY_W, self.DISPLAY_H)) #shows player what we are drawing
        self.font_name = None  # Using default system font
        self.font = pygame.font.Font(self.font_name, 32) #use default system font with size 32
        self.BLACK, self.WHITE, self.GREEN, self.RED, self.BLUE = (0, 0, 0), (255, 255, 255), (0, 100, 0), (200, 0, 0), (0, 0, 200) #colors
        # Load and scale background images
        self.background_image = pygame.image.load("menu/CardBall.png").convert()
        self.background_image = pygame.transform.scale(self.background_image, (self.DISPLAY_W, self.DISPLAY_H))
        self.field_image = pygame.image.load("menu/1.png").convert()
        self.field_image = pygame.transform.scale(self.field_image, (self.DISPLAY_W, self.DISPLAY_H))
        self.instructions_image = pygame.image.load("menu/Instructions.png").convert()
        self.instructions_image = pygame.transform.scale(self.instructions_image, (self.DISPLAY_W, self.DISPLAY_H))
        self.options_image = pygame.image.load("menu/Instructions (1).png").convert()
        self.options_image = pygame.transform.scale(self.options_image, (self.DISPLAY_W, self.DISPLAY_H))
        self.options_menu = OptionsMenu(self)
        self.instructions_menu = InstructionsMenu(self)
        self.main_menu = MainMenu(self)
        self.curr_menu = self.main_menu #current menu

    def game_loop(self): #performs the game functions
        while self.playing:
            self.check_events()
            if self.BACK_KEY:
                self.playing = False #breaks the while loop without turning off the game
            self.display.fill(self.BLACK) # Clear the screen first
            self.display.blit(self.field_image, (0, 0)) # Draw the field image
            self.window.blit(self.display, (0, 0)) #to align the display with the window
            pygame.display.update() #updates the screen
            self.reset() #resets the keys

    #checks for player input but going through all list of everything a player can input
    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                self.curr_menu.run_display = False #stops current menu from running
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
                if event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = True
                if event.key == pygame.K_UP:
                    self.UP_KEY = True
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True

    def reset(self): #resets the keys after they have been clicked
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False

    #draws text to the screen
    def draw_text(self, text, size, color, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.display.blit(text_surface, text_rect)
