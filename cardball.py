from card import Card
from card_state import CardState
from deck import Deck

CARD_SUITS = ["Clubs", "Diamonds", "Spades", "Hearts"]
CARD_RANKS = ["6", "7", "8", "9", "10", "J", "Q", "K", "A"]


if __name__ == "__main__":
    deck = Deck(CARD_SUITS, CARD_RANKS)
    print(deck)
    print(len(deck))
    print(deck.is_empty())


