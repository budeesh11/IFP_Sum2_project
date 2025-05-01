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
    

        
class Main_Card_Deck(): # Creating the main deck with all the suits and ranks, then shuffles
    def __init__(self):
        self.main_deck = [Card(i, suite, rank) for i, (suite, rank) in enumerate((suite, rank) for suite in card_suite() for rank in card_rank())]
        random.shuffle(self.main_deck)

    def player_deck(self):
        player_deck = self.main_deck[:18]  # Takes the first 18 cards of main_deck
        self.main_deck = self.main_deck[18:]  # Removes them from main_deck
        return player_deck

    def computer_deck(self):
        computer_deck = self.main_deck # Computer takes the remainder of the cards
        return computer_deck



# Handles the game's main logic
class Game_Logic():

    # Creates an instance of the player and computer deck respectively
    def __init__(self, main_deck):
        self.player_deck = main_deck.player_deck()        
        self.computer_deck = main_deck.computer_deck()
        self.player_active_cards = []
        self.computer_active_cards = []
        self.attacked_cards = {}
        self.draw = []
        
        # PLayer - true, Computer - false
        self.attacker = True
        self.attack_card = Card(-1, "temp", "temp")
        
    # Draws the first 4 cards from the player's deck
    def player_draw(self):
        if (len(self.player_active_cards) < 4 and len(self.player_deck) > 0):
            cards_to_draw = min(4 - len(self.player_active_cards), len(self.player_deck))
            self.player_active_cards.extend(self.player_deck[:cards_to_draw])
            self.player_deck = self.player_deck[cards_to_draw:]

    # Draws the first 4 cards from the computer's deck
    def computer_draw(self):
        if (len(self.computer_active_cards) < 4 and len(self.computer_deck) > 0):
            cards_to_draw = min(4 - len(self.computer_active_cards), len(self.computer_deck))
            self.computer_active_cards.extend(self.computer_deck[:cards_to_draw])
            self.computer_deck = self.computer_deck[cards_to_draw:]
    
    def get_attack_card(self):
        if (self.attacker and len(self.player_deck) > 0):
            self.attack_card = self.player_deck[0]
            self.player_deck = self.player_deck[1:]
        elif (not self.attacker and len(self.computer_deck) > 0):
            self.attack_card = self.computer_deck[0]
            self.computer_deck = self.computer_deck[1:] 
            
            
    
    
    def player_attack(self):
        ''' compare the ranks of each of the cards 
        Nested if statements for each possible outcome. win loss or draw

        Pop from the player_deck then compare that card with each of the computer's active cards then give the user the option to
        attack the possible cards

        If attack is successful then store both cards in a separate variable, using the ID as an identifier
        If draw, the computer and player each draw an additional card until one card is greater rank the other, winner takes all the cards
        If loss, both cards go to the end of the computer deck
          '''
        

        pass

    

    


def start_game_test():
    deck = Main_Card_Deck()
    game = Game_Logic(deck)
    os.system("clear")
    
    while True:
        user_input = input()
        if (user_input == "1"):
            print()
            print("ACTIVE PLAYER CARDS")
            for card in game.player_active_cards:
                print("Id: " + str(card.id) + " Suite: " + card.card_suite + " Rank: " + card.card_rank)
            print("ACTIVE COMPUTER CARDS")
            for card in game.computer_active_cards:
                print("Id: " + str(card.id) + " Suite: " + card.card_suite + " Rank: " + card.card_rank)

            print("Player Deck")
            for card in game.player_deck:
                print("Id: " + str(card.id) + " Suite: " + card.card_suite + " Rank: " + card.card_rank)
            print("Computer Deck")
            for card in game.computer_deck:
                print("Id: " + str(card.id) + " Suite: " + card.card_suite + " Rank: " + card.card_rank)
            
            print("Attack card")
            print("Id: " + str(game.attack_card.id) + " Suite: " + game.attack_card.card_suite + " Rank: " + game.attack_card.card_rank)
     
        if (user_input == "2"):
            game.player_draw()
            game.computer_draw()
        if (user_input == "3"):
            game.get_attack_card()
            print("Attack card")
            print("Id: " + str(game.attack_card.id) + " Suite: " + game.attack_card.card_suite + " Rank: " + game.attack_card.card_rank)
        if (user_input == "4"):
            print("Move change")
            game.attacker = not game.attacker
        if (user_input == "5"):
            while True:
                user_input = input()
                if (user_input == "1"):
                    game.player_draw()
                    game.computer_draw()
                    game.get_attack_card()
                    print()
                    print("Cards left: " + str(len(game.computer_deck)))
                    print("    " + str(game.computer_active_cards[0].card_suite[0]) + game.computer_active_cards[0].card_rank + "  " + str(game.computer_active_cards[1].card_suite[0]) + game.computer_active_cards[1].card_rank + "  " + str(game.computer_active_cards[2].card_suite[0]) + game.computer_active_cards[2].card_rank)
                    print()
                    print("Atk:    " + str(game.attack_card.card_suite[0]) + game.attack_card.card_rank)
                    print()
                    print("    " + str(game.player_active_cards[0].card_suite[0]) + game.player_active_cards[0].card_rank + "  " + str(game.player_active_cards[1].card_suite[0]) + game.player_active_cards[1].card_rank + "  " + str(game.player_active_cards[2].card_suite[0]) + game.player_active_cards[2].card_rank)
                    print("Cards left: " + str(len(game.player_deck)))

                    
        


if __name__ == "__main__":
    start_game_test()
