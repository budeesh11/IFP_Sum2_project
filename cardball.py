from card import Card
from card_state import CardState
from deck import Deck
from player import Player
from game_engine import GameEngine
from game_cli import GameCLI

import os

CARD_SUITS = ["Clubs", "Diamonds", "Spades", "Hearts"]
CARD_RANKS = ["6", "7", "8", "9", "10", "J", "Q", "K", "A"]


if __name__ == "__main__":
    # Testing
    deck = Deck(CARD_SUITS, CARD_RANKS)
    # Create decks for computer and player
    player_deck = deck.draw(18)
    computer_deck = deck.draw(18)

    # players creation
    player = Player("Player", player_deck)
    computer = Player("Computer", computer_deck)
    
    game_engine = GameEngine(player, computer, CARD_SUITS, CARD_RANKS)
    # TODO: temp ui because it will be changed to pygame later
    game_interface = GameCLI(game_engine)
    
    os.system("clear")
    while True:
        game_engine.change_turn()
        
        game_interface.display_game_state()

        move = input("Defender (1-3) and goalkeeper (0)")


