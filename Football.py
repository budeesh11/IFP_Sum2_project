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

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Football Card Game - Improved Version")
font = pygame.font.SysFont(None, FONT_SIZE)
clock = pygame.time.Clock()

