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

CARDS_ORDER = ["6", "7", "8", "9", "10", "J", "Q", "K", "A"]

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
    return ["6", "7", "8", "9", "10", "J", "Q", "K", "A"]

# Creating a single card object with all its attributes
class Card:
    def __init__(self, id, card_suite, card_rank):
        self.id = id
        self.card_suite = card_suite
        self.card_rank = card_rank
        self.beaten = False
    

        
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
            
        def computer_attack(self):
            
            ''' Computer will draw a card from its deck and attack the players cards.
                It will choose which card to attack based on the number of the players cards and it will attack the biggest card that it can beat
                if it can beat any. If it cannot beat any then the attack will fail and the computer will lose the card to the players deck
                if it can beat a card then the computer will win the card and add it to its deck, if computer beats goalkeeper then computer scores a goal
                whichever side reaches 3 goals first wins the game
            '''
            self.reference_deck = [Card(i, suite, rank) for i, (suite, rank) in enumerate((suite, rank) for suite in card_suite() for rank in card_rank())] # Deck ordered in terms of Rank
            
            self.attack_card_reference = None
            for card in self.reference_deck:
                if card.card_rank == self.attack_card.card_rank:
                    self.attack_card_reference = card
                    break

            player_cards_reference = []
            for card in self.player_active_cards:
                for ref_card in self.reference_deck:
                    if ref_card.card_rank == card.card_rank:
                        player_cards_reference.append((ref_card, card))
                        break

            target_card = None
            target_ref = None
            for ref_card, active_card in player_cards_reference:
                if self.attack_card_reference.id > ref_card.id:
                    if target_ref is None or ref_card.id > target_ref.id:
                        target_ref = ref_card
                        target_card = active_card
                
            #execute attack
            if target_card < self.attack_card_reference.id:
                print(f"Computer attacks with {self.attack_card.card_rank} against {target_card.card_rank}")
                self.attacked_cards[self.attack_card] = target_card
                self.player_active_cards.remove(target_card)
                print("Attack Successful")
                return True
                
            elif any(ref_card[0].id == self.attack_card_reference.id for ref_card in player_cards_reference):
                #handle draw case
                draw_card = next(card for ref, card in player_cards_reference 
                                if ref.id == self.attack_card_reference.id)
                print(f"It's a tie between {self.attack_card.card_rank} and {draw_card.card_rank}!")
                draw_pile = [self.attack_card, draw_card]
                self.player_active_cards.remove(draw_card)
                
                while True:
                    if len(self.computer_deck) == 0 or len(self.player_deck) == 0:
                        break
                        
                    computer_draw = self.computer_deck.pop(0)
                    player_draw = self.player_deck.pop(0)
                    draw_pile.extend([computer_draw, player_draw])
                    
                    #get references for drawn cards
                    comp_ref = next(card for card in self.reference_deck 
                                if card.card_rank == computer_draw.card_rank)
                    player_ref = next(card for card in self.reference_deck 
                                    if card.card_rank == player_draw.card_rank)
                                    
                    print(f"Draw cards - Computer: {computer_draw.card_rank}, Player: {player_draw.card_rank}")
                    
                    if comp_ref.id > player_ref.id:
                        print("Computer wins the draw!")
                        self.computer_deck.extend(draw_pile)
                        break
                    elif comp_ref.id < player_ref.id:
                        print("Player wins the draw!")
                        self.player_deck.extend(draw_pile)
                        break
                    else:
                        print("Another tie! Drawing again...")
                        continue
                        
            else:
                print(f"Computer attack failed with {self.attack_card.card_rank}")
                self.player_deck.append(self.attack_card)
                return False

        pass
    
    def _check_valid_attack(self, attacker, target) -> bool:
        attack_card_value = CARDS_ORDER.index(str(attacker.card_rank))
        target_card_value = CARDS_ORDER.index(str(target.card_rank))
        if (attack_card_value == 0 and target_card_value == 8):
            return True
        return attack_card_value > target_card_value

    def _goalkeeper(self):
        for i in range(len(self.computer_active_cards)):
            if (not self.computer_active_cards[i].beaten):
                return False
            else:
                return True
    
    def proper_attack(self, target):
        if (self._check_valid_attack(self.attack_card, target) and target.beaten == False):
            self.attacked_cards[self.attack_card] = target
            self.get_attack_card()
            print("Success")
            return True
        else:
            self.computer_deck.append(self.attack_card)
            self._move_change()
            print("Fail")
            return False
    
    def _move_change(self):
        # Player move end
        if (self.attacker):
            for attack_card, target_card in self.attacked_cards.items():
                self.player_deck.append(attack_card)
                self.player_deck.append(target_card) 
            
            self.computer_active_cards = [card for card in self.computer_active_cards if not card.beaten]
            for card in self.player_deck:
                card.beaten = False
            self.computer_draw()
            
            self.attacked_cards.clear()
        #TODO
        # self.attacker = not self.attacker
        self.get_attack_card()

            
        
    
        
       
        

        

    

    


def start_game_test():
    deck = Main_Card_Deck()
    game = Game_Logic(deck)
    os.system("clear")

    def temp_state_game():
        print()
        print("Cards left: " + str(len(game.computer_deck)))
        
        if len(game.computer_active_cards) > 0:
            print("    " + str(game.computer_active_cards[0].card_suite[0]) + game.computer_active_cards[0].card_rank + 
                  ("__" if game.computer_active_cards[0].beaten else ""))
        else:
            print("    No goalkeeper")
        
        defender_line = "    "
        if len(game.computer_active_cards) > 1:
            defender_line += str(game.computer_active_cards[1].card_suite[0]) + game.computer_active_cards[1].card_rank + \
                           ("__" if game.computer_active_cards[1].beaten else "")
        if len(game.computer_active_cards) > 2:
            defender_line += "  " + str(game.computer_active_cards[2].card_suite[0]) + game.computer_active_cards[2].card_rank + \
                           ("__" if game.computer_active_cards[2].beaten else "")
        if len(game.computer_active_cards) > 3:
            defender_line += "  " + str(game.computer_active_cards[3].card_suite[0]) + game.computer_active_cards[3].card_rank + \
                           ("__" if game.computer_active_cards[3].beaten else "")
        print(defender_line)
        
        print()
        print("Atk:    " + str(game.attack_card.card_suite[0]) + game.attack_card.card_rank)
        print()
        
        player_defender_line = "    "
        if len(game.player_active_cards) > 1:
            player_defender_line += str(game.player_active_cards[1].card_suite[0]) + game.player_active_cards[1].card_rank
        if len(game.player_active_cards) > 2:
            player_defender_line += "  " + str(game.player_active_cards[2].card_suite[0]) + game.player_active_cards[2].card_rank
        if len(game.player_active_cards) > 3:
            player_defender_line += "  " + str(game.player_active_cards[3].card_suite[0]) + game.player_active_cards[3].card_rank
        print(player_defender_line)
        
        if len(game.player_active_cards) > 0:
            print("    " + str(game.player_active_cards[0].card_suite[0]) + game.player_active_cards[0].card_rank)
        else:
            print("    No goalkeeper")
        
        print("Cards left: " + str(len(game.player_deck)))
        print("Attack:")
        print("Defender: 1-3")
        print("Goalkeeper: 0 (Only after beating all defenders)")
    
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
            game.player_attack()
        if (user_input == "3"):
            game.computer_draw()
            game.get_attack_card()
            #print("Attack card")
            #print("Id: " + str(game.attack_card.id) + " Suite: " + game.attack_card.card_suite + " Rank: " + game.attack_card.card_rank)
            game.player_attack()
            

        if (user_input == "4"):
            print("Move change")
            game.attacker = not game.attacker
        if (user_input == "5"):
            game.player_draw()
            game.computer_draw()
            game.get_attack_card()
            temp_state_game()
            while True:
                user_input = input()
                match user_input:
                    case "1":
                        if len(game.computer_active_cards) > 1:
                            if (game.proper_attack(game.computer_active_cards[1])):
                                game.computer_active_cards[1].beaten = True
                        else:
                            print("No defender at position 1")
                        temp_state_game()
                    case "2":
                        if len(game.computer_active_cards) > 2:
                            if (game.proper_attack(game.computer_active_cards[2])):
                                game.computer_active_cards[2].beaten = True
                        else:
                            print("No defender at position 2")
                        temp_state_game()
                    case "3":
                        if len(game.computer_active_cards) > 3:
                            if (game.proper_attack(game.computer_active_cards[3])):
                                game.computer_active_cards[3].beaten = True
                        else:
                            print("No defender at position 3")
                        temp_state_game()
                    case "0":
                        if len(game.computer_active_cards) > 0:
                            if (game.proper_attack(game.computer_active_cards[0])):
                                game.computer_active_cards[0].beaten = True
                        else:
                            print("No goalkeeper")
                        temp_state_game()
                    case _:
                        break

                
        else:
            break

                    
        


if __name__ == "__main__":
    start_game_test()
