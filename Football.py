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
CARD_WIDTH, CARD_HEIGHT = 120, 160
CARD_SPACING = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 100, 0)
RED = (200, 0, 0)
BLUE = (0, 0, 200)
GRAY = (200, 200, 200)
FONT_SIZE = 24
TURN_TIME = 30  # seconds per turn


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

# Returns a list for the card suites
def card_suite():
    return ["Clubs", "Diamonds", "Spades", "Hearts"]

# Returns a list of the card ranks
def card_rank():
    return ["6", "7", "8", "9", "10", "K", "Q", "J", "A"]

# Creating a single card object with all its attributes
class Card:
    def __init__(self, card_suite, card_rank):
        self.id = id
        self.card_suite = card_suite
        self.card_rank = card_rank
    
   # def __str__(self):
    #    return f"{self.card_rank} of {self.card_suite }" 

 # Creating the main deck with all the possible combinations       
class Main_Card_Deck():
    def __init__(self):
        self.main_deck = [] 
        self.main_deck = [Card(suite, rank) for suite in card_suite() for rank in card_rank() ] # For loop create a card object for every element in each of the card functions 

    def player_deck(self):

        player_deck = []

        while len(self.main_deck) != 18:
            x = 0
            player_deck =  player_deck.append(self.main_deck[x])
            self.main_deck.pop(x)
            x += 1

        return player_deck 

    def computer_deck(self):

        computer_deck = self.main_deck
        return computer_deck

# Player Decks
class Computer_Deck(Main_Card_Deck):
    def __init__(self):
        super().__init__()
    
    pass

class Player_Deck(Main_Card_Deck):
    def __init__(self):
        
        pass


if __name__ == "__main__":
    deck = Main_Card_Deck()
    print(deck.player_deck.__str__())
