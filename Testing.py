
# Returns a list for the card suites
def card_suite():
    return ["Clubs", "Diamonds", "Spades", "Hearts"]

# Returns a list of the card ranks
def card_rank():
    return ["6", "7", "8", "9", "10", "K", "Q", "J", "A"]

# Creating a single card object with all its attributes
class Card:
    def __init__(self, card_suite, card_rank):
        self.id = id
        self.card_suite = card_suite
        self.card_rank = card_rank
    
   

 # Creating the main deck with all the possible combinations       
class Main_Card_Deck():
    def __init__(self):
        self.main_deck = [] 
        self.main_deck = [Card(suite, rank) for suite in card_suite() for rank in card_rank() ] # For loop create a card object for every element in each of the card functions 

    def player_deck(self):

        player_deck = []

        while len(self.main_deck) != 18:
            x = 0
            player_deck =  player_deck.append(self.main_deck[x])
            self.main_deck.pop(x)
            x += 1

        return player_deck 

    def computer_deck(self):

        computer_deck = self.main_deck
        return computer_deck

# Player Decks
class Computer_Deck(Main_Card_Deck):
    def __init__(self):
        super().__init__()
    
    pass

class Player_Deck(Main_Card_Deck):
    def __init__(self):
        
        pass


if __name__ == "__main__":
    deck = Main_Card_Deck()
    print(deck.player_deck.__str__())

