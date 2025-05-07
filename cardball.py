from card import Card
from card_state import CardState
from deck import Deck
from player import Player
from game_engine import GameEngine
from game_cli import GameCLI

import os
import time

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
    
    while True:
        game_engine.change_turn()
        while True:
        
            # os.system("clear")
            game_interface.display_game_state()

            
            if game_engine.attacker.name == "Computer":
                target_index = game_engine.computer_attack()
            else:
                target_index = input("Defender (1-3) and goalkeeper (0): ")
                if target_index == "":
                    game_engine.attack_end()
                    break
                    
            if target_index in ["1", "2", "3", "0"]:
                result = game_engine.attack_handle(int(target_index))
                print("Result: " + str(result))
                
                time.sleep(1)
                
                if result == "Fail" or not game_engine.valid_for_next_attack():
                    break
            
            
        


