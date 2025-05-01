import pygame, sys
pygame.init()

SCREEN_W, SCREEN_H = 1920, 1080
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))

PLAY = "play"
RULES = "rules"
SETTINGS = "settings"
MENU = "menu"
current_state = MENU