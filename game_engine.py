# This import as I understand gives ability to work with methods and attributes of a Player class
from player import Player
from card_state import CardState

class gameEngine():
    def __init__(self, player: Player, computer: Player):
        self.player = player
        self.computer = computer
        self.attacker = player
        self.defender = computer
        
        self.attack_card = None
        self.draw_cards_storage = []
    
    # This method should be completed and if changed can be still used like this
    def change_turn(self):
        self.attacker, self.defender = self.defender, self.attacker
        # I have changed the process of move change and how cards are moved between players deck and other storages
        self.attack_card = None
        self.attacker.draw_active_cards()
        self.defender.draw_active_cards()
    
    # index is the index of target card in active cards of opponent
    def attack_handle(self, target_card_index):
        if self.attack_card == None:
            if self.attacker.deck.is_empty():
                return "DEBUG: No cards left in deck of " + self.attacker
            self.attack_card = self.attacker.deck.pop(0)
        
        # Protection for possible invalid target choice. Helpful even when I will lock most of dangerous inputs
        try:
            target = self.defender.active_cards[target_card_index]
        except:
            return "DEBUG: Invalid target on index - " + target_card_index
        
        
        if target_card_index == 0:
            if not self._goalkeeper_attack_validity(target_card_index):
                return
                
    
    #TODO Goalkeeper protection from invalid attack will be probably reworked
    def _goalkeeper_attack_validity(self, target_index):
        if target_index == 0:
            for defender_position in [1, 2, 3]:
                if defender_position < len(self.defender.active_cards):
                    if self.defender.active_cards[defender_position].card_state != CardState.BEATEN:
                        return False, "Cannot attack goalkeeper until defenders are beaten"
        
        return True, "Valid attack"
        
    