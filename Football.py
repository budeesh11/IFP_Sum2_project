import pygame
import random
import sys
import os
from typing import List, Tuple, Optional
from enum import Enum
import time

# initialising pygame

pygame.init()
pygame.mixer.init()

# constants for window
SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 800

class game():
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Football Game")
        self.clock = pygame.time.Clock()
        self.running = True
        self.font = pygame.font.Font(None, 36)
        self.background_color = (0, 128, 0)  # Green background for the football field

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.screen.fill(self.background_color)
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

    def draw_cards(self):
        card_list = ["1S", "2S", "3S", "4S", "5S", "6S", "7S", "8S", "9S", "10S", "JS", "QS", "KS", "AS",
                     "1H", "2H", "3H", "4H", "5H", "6H", "7H", "8H", "9H", "10H", "JH", "QH", "KH", "AH",
                     "1C", "2C", "3C", "4C", "5C", "6C", "7C", "8C", "9C", "10C", "JC", "QC", "KC", "AC",
                     "1D", "2D", "3D", "4D", "5D", "6D", "7D", "8D", "9D", "10D", "JD", "QD", "KD", "AD",]



