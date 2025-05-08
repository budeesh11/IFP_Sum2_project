# This import as I understand gives ability to work with methods and attributes of a Player class
from player import Player
from card_state import CardState
from card import Card

import copy
import time

class GameEngine():
    def __init__(self, player: Player, computer: Player, CARD_SUITS: list, CARD_RANKS: list):
        self.player = player
        self.computer = computer
        self.attacker = computer
        self.defender = player
        
        self.last_draw_winner = None
        
        self.CARD_SUITS = CARD_SUITS
        self.CARD_RANKS = CARD_RANKS
        
        self.attack_card = None
        self.battle_cards = []
        self.draw_pile = []
        
        self.game_running = True
    
    # This method should be completed and if changed can be still used like this
    def change_turn(self):
        
        # Add all cards that attacker won to his deck
        for card in self.battle_cards:
            card.card_state = CardState.REST
            
        self.attacker.deck.extend(self.battle_cards)
        self.battle_cards = []
        

        self.defender.active_cards = [card for card in self.defender.active_cards 
                                      if card.card_state != CardState.BEATEN]
        
        
        self.attacker, self.defender = self.defender, self.attacker
        # I have changed the process of move change and how cards are moved between players deck and other storages
        if len(self.attacker.deck) == 0:
            return "DEBUG: No cards left in deck of " + self.attacker.name
        self.attack_card = self.attacker.deck.pop(0)
            
        self.attacker.draw_active_cards()
        self.defender.draw_active_cards()
    
    # index is the index of target card in active cards of opponent
    def attack_handle(self, target_card_index: int):
        
        # Protection for possible invalid target choice. Helpful even when I will lock most of dangerous inputs
        try:
            target = self.defender.active_cards[target_card_index]
        except:
            return "DEBUG: Invalid target on index - " + str(target_card_index) + ". Attack card: " + self.attack_card.display()
        
        if target.card_state == CardState.BEATEN:
            return "Card is already beaten! Choose another target."

        if target_card_index == 0:
            for defender_position in [1, 2, 3]:
                if defender_position < len(self.defender.active_cards):
                    if self.defender.active_cards[defender_position].card_state != CardState.BEATEN:
                        return "DEBUG: Invalid attack. Attack of goalkeeper is impossible until all defenders are beaten"
        
        result = self._resolve_attack_type(target)
        return result
    
    def _resolve_attack_type(self, defender_card: Card):
        attacker_value = self.CARD_RANKS.index(self.attack_card.rank)
        defender_value = self.CARD_RANKS.index(defender_card.rank)
        
        
        if (attacker_value > defender_value) or (attacker_value == 0 and defender_value == 8):
            defender_card.card_state = CardState.BEATEN
            self.battle_cards.append(copy.copy(self.attack_card))
            self.battle_cards.append(copy.copy(defender_card))
            self._check_goal_condition()
            return "Success"
        elif attacker_value == defender_value:
            self._draw_handle(defender_card)
            return "Draw"
        else:
            self.defender.deck.append(copy.copy(self.attack_card))
            return "Fail"
    
    def valid_for_next_attack(self):
        if not self.attacker.deck:
            return False
        if all(card.card_state == CardState.BEATEN for card in self.defender.active_cards):
            return False
        
        self.attack_card = self.attacker.deck.pop(0)
        return True

    def _check_goal_condition(self):
        if not self.defender.active_cards:
            return

        cards_beaten = True
        
        for card in self.defender.active_cards:
            if card.card_state != CardState.BEATEN:
                cards_beaten = False
        
        if cards_beaten:
            self.attacker.goals += 1
            print("Goal! " + self.attacker.name + " scored!")
    
    def computer_attack(self):
        print("Computer thinks...")
        time.sleep(1)
        if not self.attack_card:
            return None
        attacker_strength = self.CARD_RANKS.index(self.attack_card.rank)
        best_index = None
        best_defender_strength = -1

        # First priority: Check if the computer has a 6 and can attack an Ace
        if attacker_strength == 0: 
            for i, defender_card in enumerate(self.defender.active_cards):
                if defender_card.card_state == CardState.BEATEN:
                    continue
                    
                if i == 0 and any(
                    j < len(self.defender.active_cards) and
                    self.defender.active_cards[j].card_state != CardState.BEATEN
                    for j in [1, 2, 3]
                ):
                    continue
                    
                defender_strength = self.CARD_RANKS.index(defender_card.rank)
                if defender_strength == 8:  #
                    return i 

        for i, defender_card in enumerate(self.defender.active_cards):
            if defender_card.card_state == CardState.BEATEN:
                continue

            if i == 0 and any(
                j < len(self.defender.active_cards) and
                self.defender.active_cards[j].card_state != CardState.BEATEN
                for j in [1, 2, 3]
            ):
                continue

            defender_strength = self.CARD_RANKS.index(defender_card.rank)

            # The goal of computer algorithm is to find and beat the highest possible card because when it will take it and after n amount of moves this card will show up
            # There is a lot of place for creating algorithm here
            # This the basic that I came with
            # It is possible to improve it like creating memory so if it remembers what card it won earlier and how many cards left until it it can use it for attack
            if attacker_strength > defender_strength:
                if defender_strength > best_defender_strength:
                    best_defender_strength = defender_strength
                    best_index = i

        # If no beatable cards, consider draw
        # TODO: if somebody wants. Try to implement so it can compare how much profit it will get for draw and maybe go for it instead of just attacking
        if best_index is None:
            for i, defender_card in enumerate(self.defender.active_cards):
                if defender_card.card_state == CardState.BEATEN:
                    continue
                if i == 0 and any(
                    j < len(self.defender.active_cards) and
                    self.defender.active_cards[j].card_state != CardState.BEATEN
                    for j in [1, 2, 3]
                ):
                    continue
                if self.CARD_RANKS.index(defender_card.rank) == attacker_strength:
                    return i

        return "" if best_index is None else best_index
    
    # Used incase there is no way to attack or you want to skip move
    def attack_end(self):
        self.defender.deck.append(copy.copy(self.attack_card))
    
    def _draw_handle(self, defender_card: Card):
        self.draw_pile = []
        self.draw_pile = [self.attack_card, copy.copy(defender_card)]
        
        if defender_card in self.defender.active_cards:
            defender_card.card_state = CardState.BEATEN
        
        while True:
            if not self.attacker.deck:
                print(f"{self.defender.name} wins the draw (attacker out of cards)")
                self.defender.deck.extend(self.draw_pile)
                break
            if not self.defender.deck:
                print(f"{self.attacker.name} wins the draw (defender out of cards)")
                self.attacker.deck.extend(self.draw_pile)
                break
            
            
            attacker_draw = self.attacker.deck.pop(0)
            defender_draw = self.defender.deck.pop(0)
            
            self.draw_pile.append(attacker_draw)
            self.draw_pile.append(defender_draw)
            
            attacker_value = self.CARD_RANKS.index(attacker_draw.rank)
            defender_value = self.CARD_RANKS.index(defender_draw.rank)

            if attacker_value > defender_value:
                print("DEBUG: " + self.attacker.name + " wins draw!")
                self.battle_cards.extend(self.draw_pile)
                self.last_draw_winner = self.attacker.name
                break
            if defender_value > attacker_value:
                print("DEBUG: " + self.defender.name + " wins draw!")
                self.defender.deck.extend(self.draw_pile)
                self.last_draw_winner = self.defender.name
                break
    
    def _check_win_condition(self):
        if self.attacker.goals == 3 or self.defender.goals == 3 or len(self.attacker.deck) == 0 or len(self.defender.deck) == 0:
            self.game_running = False
            return True
        return False

        
    
        
                
    
        
    