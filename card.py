from card_state import CardState

class Card:
    def __init__(self, id, suit, rank):
        self.id = id
        self.suit = suit
        self.rank = rank
        # Card state
        self.card_state = CardState.REST
        self.deck_side = CardState.DECK
    
    def display(self):
        return str(self.suit[0] + self.rank[0])

    def display_with_id(self):
        return str(self.id) + ". " + self.suit[0] + self.rank[0]