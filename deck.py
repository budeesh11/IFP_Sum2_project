import random
from card import Card

class Deck:
    
    def __init__(self, suits, ranks):
        self.cards = [Card(i, suit, rank) 
                      for i, (suit, rank) in enumerate((suit, rank) for suit in suits for rank in ranks)]
        random.shuffle(self.cards)
    
    def __str__(self):
        result = ""
        for card in self.cards:
            result += card.display_with_id() + " "
        return result
    
    def __len__(self):
        return len(self.cards)
