# This import as I understand gives ability to work with methods and attributes of a Player class
from player import Player
from card_state import CardState
from card import Card

class GameEngine():
    def __init__(self, player: Player, computer: Player, CARD_SUITS: list, CARD_RANKS: list):
        self.player = player
        self.computer = computer
        self.attacker = player
        self.defender = computer
        
        self.CARD_SUITS = CARD_SUITS
        self.CARD_RANKS = CARD_RANKS
        
        self.attack_card = None
        self.battle_cards = []
    
    # This method should be completed and if changed can be still used like this
    def change_turn(self):
        self.attacker, self.defender = self.defender, self.attacker
        # I have changed the process of move change and how cards are moved between players deck and other storages
        if self.attack_card == None:
            if len(self.attacker.deck) == 0:
                return "DEBUG: No cards left in deck of " + self.attacker
            self.attack_card = self.attacker.deck.pop(0)
        self.attacker.draw_active_cards()
        self.defender.draw_active_cards()
    
    # index is the index of target card in active cards of opponent
    def attack_handle(self, target_card_index):
        
        # Protection for possible invalid target choice. Helpful even when I will lock most of dangerous inputs
        try:
            target = self.defender.active_cards[target_card_index]
        except:
            return "DEBUG: Invalid target on index - " + target_card_index
        
        if target_card_index == 0:
            for defender_position in [1, 2, 3]:
                if defender_position < len(self.defender.active_cards):
                    if self.defender.active_cards[defender_position].card_state != CardState.BEATEN:
                        return "DEBUG: Invalid attack. Attack of goalkeeper is impossible until all defenders are beaten"
    
    def _resolve_attack_type(self, attacker_card: Card, defender_card: Card):
        attacker_value = self.CARD_RANKS.index(attacker_card.rank)
        defender_value = self.CARD_RANKS.index(defender_card.rank)
        
        
        if (attacker_value > defender_value) or (attacker_value == 0 and defender_value == 8):
            defender_card.card_state = CardState.BEATEN
            return "Success"
        elif attacker_value == defender_value:
            #TODO Draw situation is not completed
            return "Draw"
        else:
            #TODO
            return "Fail"
    
    def _valid_for_next_attack(self):
        if not self.attacker.deck:
            return False
        if all(card.card_state == CardState.BEATEN for card in self.defender.active_cards):
            return False
        return True
        
        
                
    
        
    