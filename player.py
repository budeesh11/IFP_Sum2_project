class Player:
    def __init__(self, name, deck: list):
        self.name = name
        self.deck = deck
        self.active_cards = []
        self.goals = 0
    
    def draw_active_cards(self):
        to_draw = min(4 - len(self.active_cards), len(self.deck))
        self.active_cards.extend(self.deck[:to_draw])
        self.deck = self.deck[to_draw:]
    
    def display_active_cards(self):
        result = ""
        for card in self.active_cards:
            result += card.display() +" "
        return result
    