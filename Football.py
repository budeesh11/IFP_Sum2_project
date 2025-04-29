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
    def __init__(self, id, card_suite, card_rank):
        self.id = id
        self.card_suite = card_suite
        self.card_rank = card_rank
    
   # def __str__(self):
    #    return f"{self.card_rank} of {self.card_suite }" 

 # Creating the main deck with all the possible combinations       
class Main_Card_Deck():
    def __init__(self):
        self.main_deck = [Card(i, suite, rank) for i, (suite, rank) in enumerate((suite, rank) for suite in card_suite() for rank in card_rank())]
        random.shuffle(self.main_deck)

    def player_deck(self):
        player_deck = self.main_deck[:18]  # First 18 cards
        self.main_deck = self.main_deck[18:]  # Remove them from main_deck
        return player_deck

    def computer_deck(self):
        computer_deck = self.main_deck
        return computer_deck

# Player Decks
class Computer_Deck():
    def __init__(self, deck):
        self.cards = deck
    
    pass

class Player_Deck():
    def __init__(self, deck):
        self.cards = deck
    
    pass

def start_game_test():
    deck = Main_Card_Deck()
    player_deck = Player_Deck(deck.player_deck())
    computer_deck = Computer_Deck(deck.computer_deck())
    print("Player Deck")
    for card in player_deck.cards:
        print("Id: " + str(card.id) + " Suite: " + card.card_suite + " Rank: " + card.card_rank)
    print("Computer Deck")
    for card in computer_deck.cards:
        print("Id: " + str(card.id) + " Suite: " + card.card_suite + " Rank: " + card.card_rank)


if __name__ == "__main__":
    start_game_test()
