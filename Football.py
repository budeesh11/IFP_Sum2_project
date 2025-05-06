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
        self.player_goal = 0
        self.computer_goal = 0

        self.game_state = "Started"
        
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
    
    def _check_valid_attack(self, attacker, target):
        attack_card_value = CARDS_ORDER.index(str(attacker.card_rank))
        target_card_value = CARDS_ORDER.index(str(target.card_rank))
        if attack_card_value == target_card_value:
            return "draw"
        if attack_card_value == 0 and target_card_value == 8:
            return True
        if attack_card_value > target_card_value:
            return True
        return False

    def _goalkeeper(self):
        for i in range(len(self.computer_active_cards)):
            if (not self.computer_active_cards[i].beaten):
                return False
            else:
                return True
    
    def proper_attack(self, target):
        result = self._check_valid_attack(self.attack_card, target)
        if result == True and not target.beaten:
            self.attacked_cards[self.attack_card] = target
            self.get_attack_card()
            print("Success")
            return True
        elif result == "draw" and not target.beaten:
            print(f"Draw between {self.attack_card.card_rank} and {target.card_rank}!")
            self._draw_situation(target)
            return "draw"
        else:
            self.computer_deck.append(self.attack_card)
            self._move_change()
            print("Fail")
            return False
    
    def _check_win_condition(self):
        if self.computer_goal == 3 or self.player_deck == 0:
            print("Computer wins!")
        elif self.player_goal == 3 or self.computer_deck == 0:
            print("Player wins!")
    
    def _goal_condition(self):
        all_beaten = True
        
        if self.attacker:
            for card in self.computer_active_cards:
                if not card.beaten:
                    all_beaten = False
                    break
                
            if all_beaten and len(self.computer_active_cards) > 0:
                for card in self.computer_active_cards:
                    self.player_deck.append(card)
                
                self.player_goal += 1
                print(f"GOAL! Player scores! Score: {self.player_goal} - {self.computer_goal}")
                self.computer_active_cards = []
            
        else:
            for card in self.player_active_cards:
                if not card.beaten:
                    all_beaten = False
                    break
                
            if all_beaten and len(self.player_active_cards) > 0:
                for card in self.player_active_cards:
                    self.computer_deck.append(card)
                
                self.computer_goal += 1
                print(f"GOAL! Computer scores! Score: {self.player_goal} - {self.computer_goal}")
                self.player_active_cards = []
        
        if all_beaten:
            self.attacked_cards.clear()
            self._move_change()
    
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
    
    def _print_draw_situation(self):
        result = ""
        for i in range(0, len(self.draw), 2):
            pair = f"{i//2 + 1}. "
            pair += f"{self.draw[i].card_suite[0]}{self.draw[i].card_rank}"
            if i + 1 < len(self.draw):
                pair += f", {self.draw[i+1].card_suite[0]}{self.draw[i+1].card_rank}"
            result += pair + " "
        return result.strip()
        
    def temp_state_game(self):
        print()
        print("Cards left: " + str(len(self.computer_deck)))
        
        if len(self.computer_active_cards) > 0:
            print("    " + str(self.computer_active_cards[0].card_suite[0]) + self.computer_active_cards[0].card_rank + 
                  ("__" if self.computer_active_cards[0].beaten else ""))
        else:
            print("    No goalkeeper")
        
        defender_line = "    "
        if len(self.computer_active_cards) > 1:
            defender_line += str(self.computer_active_cards[1].card_suite[0]) + self.computer_active_cards[1].card_rank + \
                           ("__" if self.computer_active_cards[1].beaten else "")
        if len(self.computer_active_cards) > 2:
            defender_line += "  " + str(self.computer_active_cards[2].card_suite[0]) + self.computer_active_cards[2].card_rank + \
                           ("__" if self.computer_active_cards[2].beaten else "")
        if len(self.computer_active_cards) > 3:
            defender_line += "  " + str(self.computer_active_cards[3].card_suite[0]) + self.computer_active_cards[3].card_rank + \
                           ("__" if self.computer_active_cards[3].beaten else "")
        print(defender_line)
        
        print()
        print("Atk:    " + str(self.attack_card.card_suite[0]) + self.attack_card.card_rank)
        self._print_draw_situation()
        print()
        
        player_defender_line = "    "
        if len(self.player_active_cards) > 1:
            player_defender_line += str(self.player_active_cards[1].card_suite[0]) + self.player_active_cards[1].card_rank
        if len(self.player_active_cards) > 2:
            player_defender_line += "  " + str(self.player_active_cards[2].card_suite[0]) + self.player_active_cards[2].card_rank
        if len(self.player_active_cards) > 3:
            player_defender_line += "  " + str(self.player_active_cards[3].card_suite[0]) + self.player_active_cards[3].card_rank
        print(player_defender_line)
        
        if len(self.player_active_cards) > 0:
            print("    " + str(self.player_active_cards[0].card_suite[0]) + self.player_active_cards[0].card_rank)
        else:
            print("    No goalkeeper")
        
        print("Cards left: " + str(len(self.player_deck)))
        print("Defender: 1-3")
        print("Goalkeeper: 0 (Only after beating all defenders)")
        print(str(self.player_goal) + " : " + str(self.computer_goal))
    
    def temp_state_game_draw(self):
        print()
        print("Cards left: " + str(len(self.computer_deck)))
        
        if len(self.computer_active_cards) > 0:
            print("    " + str(self.computer_active_cards[0].card_suite[0]) + self.computer_active_cards[0].card_rank + 
                  ("__" if self.computer_active_cards[0].beaten else ""))
        else:
            print("    No goalkeeper")
        
        defender_line = "    "
        if len(self.computer_active_cards) > 1:
            defender_line += str(self.computer_active_cards[1].card_suite[0]) + self.computer_active_cards[1].card_rank + \
                           ("__" if self.computer_active_cards[1].beaten else "")
        if len(self.computer_active_cards) > 2:
            defender_line += "  " + str(self.computer_active_cards[2].card_suite[0]) + self.computer_active_cards[2].card_rank + \
                           ("__" if self.computer_active_cards[2].beaten else "")
        if len(self.computer_active_cards) > 3:
            defender_line += "  " + str(self.computer_active_cards[3].card_suite[0]) + self.computer_active_cards[3].card_rank + \
                           ("__" if self.computer_active_cards[3].beaten else "")
        print(defender_line)
        
        print()
        print("Draw:    " + self._print_draw_situation())
        print()
        
        player_defender_line = "    "
        if len(self.player_active_cards) > 1:
            player_defender_line += str(self.player_active_cards[1].card_suite[0]) + self.player_active_cards[1].card_rank
        if len(self.player_active_cards) > 2:
            player_defender_line += "  " + str(self.player_active_cards[2].card_suite[0]) + self.player_active_cards[2].card_rank
        if len(self.player_active_cards) > 3:
            player_defender_line += "  " + str(self.player_active_cards[3].card_suite[0]) + self.player_active_cards[3].card_rank
        print(player_defender_line)
        
        if len(self.player_active_cards) > 0:
            print("    " + str(self.player_active_cards[0].card_suite[0]) + self.player_active_cards[0].card_rank)
        else:
            print("    No goalkeeper")
        
        print("Cards left: " + str(len(self.player_deck)))
        print("Defender: 1-3")
        print("Goalkeeper: 0 (Only after beating all defenders)")
    
    def handle_defender_attack(self, defender_index):
        if len(self.computer_active_cards) > defender_index:
            result = self.proper_attack(self.computer_active_cards[defender_index])
            if result == True:
                self.computer_active_cards[defender_index].beaten = True
            elif result == "draw":
                self.temp_state_game_draw()
                
        else:
            if defender_index == 0:
                print("No goalkeeper")
            else:
                print(f"No defender at position {defender_index}")
        self._goal_condition()
        self._debug_card_count()
        self.temp_state_game()
    
    def _draw_situation(self, attacked_card):
        draw = True
        winner = ""
        self.draw.append(self.attack_card)
        self.draw.append(attacked_card)
        while draw:
            self.get_attack_card()
            self.draw.append(self.attack_card)
            
            if self.attacker:
                if self.computer_deck:
                    self.draw.append(self.computer_deck.pop(0))
                else:
                    print("Computer deck is empty!")
                    winner = "P"
                    break
            else:
                if self.player_deck:
                    self.draw.append(self.player_deck.pop(0))
                else:
                    print("Player deck is empty!")
                    winner = "C"
                    break
            
            attacker = CARDS_ORDER.index(str(self.draw[-2].card_rank))
            defender = CARDS_ORDER.index(str(self.draw[-1].card_rank))
            
            if attacker > defender:
                if self.attacker:
                    winner = "P"
                else:
                    winner = "C"
                draw = False
            elif attacker < defender:
                if not self.attacker:
                    winner = "P"
                else:
                    winner = "C"
                draw = False
        if winner == "P":
            for draw_card in self.draw:
                if draw_card in self.player_active_cards or draw_card in self.computer_active_cards:
                    draw_card.beaten = True
            self.player_deck.extend(self.draw)
        elif winner == "C":
            for draw_card in self.draw:
                if draw_card in self.player_active_cards or draw_card in self.computer_active_cards:
                    draw_card.beaten = True
            self.computer_deck.extend(self.draw)
        
        if winner == "P" and not self.attacker:
            self._move_change()
            return
        elif winner == "C" and self.attacker:
            self._move_change()
            return
        self._print_draw_situation()  
        print(f"Draw winner: {winner}")
        self.draw.clear()
        self.get_attack_card()

    # Debug method. Hard to count every time 
    def _debug_card_count(self):
        total = (len(self.computer_deck) + len(self.computer_active_cards) + 
                 len(self.player_deck) + len(self.player_active_cards) + 
                 (1 if self.attack_card.id != -1 else 0) +
                 len(self.draw)
                 )
        print(f"DEBUG: Total cards: {total}")

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
            game.temp_state_game()
            while True:
                user_input = input()
                match user_input:
                    case "1":
                        game.handle_defender_attack(1)
                    case "2":
                        game.handle_defender_attack(2)
                    case "3":
                       game.handle_defender_attack(3)
                    case "0":
                        game.handle_defender_attack(0)
                    case _:
                        break

                
        else:
            break

                    
        





if __name__ == "__main__":
    start_game_test()


-1 -1
+4 +0
-1 -1