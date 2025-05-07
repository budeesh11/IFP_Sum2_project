# This import as I understand gives ability to work with methods and attributes of a Player class
from player import Player
from card_state import CardState
from card import Card

import copy

class GameEngine():
    def __init__(self, player: Player, computer: Player, CARD_SUITS: list, CARD_RANKS: list):
        self.player = player
        self.computer = computer
        self.attacker = computer
        self.defender = player
        
        self.CARD_SUITS = CARD_SUITS
        self.CARD_RANKS = CARD_RANKS
        
        self.attack_card = None
        self.battle_cards = []
    
    # This method should be completed and if changed can be still used like this
    def change_turn(self):
        
        # Add all cards that attacker won to his deck
        for card in self.battle_cards:
            card.card_state = CardState.REST
            
        self.attacker.deck.extend(self.battle_cards)
        self.battle_cards = []
        
        for card in self.defender.active_cards:
            if card.card_state == CardState.BEATEN:
                self.defender.active_cards.remove(card)
        
        
        self.attacker, self.defender = self.defender, self.attacker
        # I have changed the process of move change and how cards are moved between players deck and other storages
        if len(self.attacker.deck) == 0:
            return "DEBUG: No cards left in deck of " + self.attacker
        self.attack_card = self.attacker.deck.pop(0)
            
        self.attacker.draw_active_cards()
        self.defender.draw_active_cards()
    
    # index is the index of target card in active cards of opponent
    def attack_handle(self, target_card_index: int):
        
        # Protection for possible invalid target choice. Helpful even when I will lock most of dangerous inputs
        try:
            target = self.defender.active_cards[target_card_index]
        except:
            return "DEBUG: Invalid target on index - " + target_card_index + ". Attack card: " + self.attack_card.display()
        
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
            #TODO Draw situation is not completed
            return "Draw"
        else:
            #TODO
            return "Fail"
    
    def valid_for_next_attack(self):
        if not self.attacker.deck:
            return False
        if all(card.card_state == CardState.BEATEN for card in self.defender.active_cards):
            return False
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

    
    
        
                
    
        
    