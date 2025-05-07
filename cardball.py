from card import Card
from card_state import CardState
from deck import Deck

CARD_SUITS = ["Clubs", "Diamonds", "Spades", "Hearts"]
CARD_RANKS = ["6", "7", "8", "9", "10", "J", "Q", "K", "A"]


if __name__ == "__main__":
    # Testing
    deck = Deck(CARD_SUITS, CARD_RANKS)
    # Create decks for computer and player
    player_deck = deck.draw(18)
    computer_deck = deck.draw(18)
    for card in player_deck:
        print(card.display())
    for card in computer_deck:
        print(card.display())
    print(deck.is_empty())
    print(len(deck))


