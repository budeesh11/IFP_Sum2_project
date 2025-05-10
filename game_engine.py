# This import as I understand gives ability to work with methods and attributes of a Player class
from player import Player
from card_state import CardState
from card import Card

import copy
import time

class GameEngine():
    def __init__(self, player: Player, computer: Player, CARD_SUITS: list, CARD_RANKS: list):
        self.player = player
        self.computer = computer
        self.attacker = computer
        self.defender = player
        
        self.last_draw_winner = None
        self.last_draw_cards = []  # Store cards involved in the last draw
        
        self.CARD_SUITS = CARD_SUITS
        self.CARD_RANKS = CARD_RANKS
        
        self.attack_card = None
        self.battle_cards = []
        self.draw_pile = []
        
        self.game_running = True
    
    # This method should be completed and if changed can be still used like this
    def change_turn(self):
        
        # Add all cards that attacker won to his deck
        for card in self.battle_cards:
            card.card_state = CardState.REST
            
        self.attacker.deck.extend(self.battle_cards)
        self.battle_cards = []
        

        self.defender.active_cards = [card for card in self.defender.active_cards 
                                      if card.card_state != CardState.BEATEN]
        
        
        self.attacker, self.defender = self.defender, self.attacker
        # I have changed the process of move change and how cards are moved between players deck and other storages
        if len(self.attacker.deck) == 0:
            return "DEBUG: No cards left in deck of " + self.attacker.name
        self.attack_card = self.attacker.deck.pop(0)
            
        self.attacker.draw_active_cards()
        self.defender.draw_active_cards()
    
    # index is the index of target card in active cards of opponent
    def attack_handle(self, target_card_index: int):
        
        # Protection for possible invalid target choice. Helpful even when I will lock most of dangerous inputs
        try:
            target = self.defender.active_cards[target_card_index]
        except:
            return "DEBUG: Invalid target on index - " + str(target_card_index) + ". Attack card: " + self.attack_card.display()
        
        if target.card_state == CardState.BEATEN:
            return "Card is already beaten! Choose another target."

        if target_card_index == 0:
            for defender_position in [1, 2, 3]:
                if defender_position < len(self.defender.active_cards):
                    if self.defender.active_cards[defender_position].card_state != CardState.BEATEN:
                        return "DEBUG: Invalid attack. Attack of goalkeeper is impossible until all defenders are beaten"
        
        result = self._resolve_attack_type(target)
        return result
    
    def _resolve_attack_type(self, defender_card: Card):
        attacker_value = self.CARD_RANKS.index(self.attack_card.rank)
        defender_value = self.CARD_RANKS.index(defender_card.rank)
        
        # Special rule: Ace beats everything except 6
        # Scenario for when attacking card is an ace
        if self.attack_card.rank == 'A':
            if defender_card.rank == '6':  # 6 beats Ace
                self.defender.deck.append(copy.copy(self.attack_card))
                return "Fail"
            elif defender_card.rank == 'A':  # Ace vs Ace is a draw
                self._draw_handle(defender_card)
                return "Draw"
            else:  # Ace beats everything else
                defender_card.card_state = CardState.BEATEN
                self.battle_cards.append(copy.copy(self.attack_card))
                self.battle_cards.append(copy.copy(defender_card))
                self._check_goal_condition()
                return "Success"
        # If defender has Ace
        elif defender_card.rank == 'A':
            if self.attack_card.rank == '6':  # 6 beats Ace
                defender_card.card_state = CardState.BEATEN
                self.battle_cards.append(copy.copy(self.attack_card))
                self.battle_cards.append(copy.copy(defender_card))
                self._check_goal_condition()
                return "Success"
            else:  # Ace beats everything else
                self.defender.deck.append(copy.copy(self.attack_card))
                return "Fail"
        # Normal comparison for other cards
        elif attacker_value > defender_value:
            defender_card.card_state = CardState.BEATEN
            self.battle_cards.append(copy.copy(self.attack_card))
            self.battle_cards.append(copy.copy(defender_card))
            self._check_goal_condition()
            return "Success"
        elif attacker_value == defender_value:
            self._draw_handle(defender_card)
            return "Draw"
        else:
            self.defender.deck.append(copy.copy(self.attack_card))
            return "Fail"
    
    def valid_for_next_attack(self):
        if not self.attacker.deck:
            return False
        if all(card.card_state == CardState.BEATEN for card in self.defender.active_cards):
            return False
        
        self.attack_card = self.attacker.deck.pop(0)
        return True

    def _check_goal_condition(self):
        if not self.defender.active_cards:
            return

        cards_beaten = True
        
        for card in self.defender.active_cards:
            if card.card_state != CardState.BEATEN:
                cards_beaten = False
        
        if cards_beaten:
            self.attacker.goals += 1
            print("Goal! " + self.attacker.name + " scored!")
    
    def computer_attack(self):
        print("Computer thinks...")
        time.sleep(1)
        if not self.attack_card:
            return None
        attacker_strength = self.CARD_RANKS.index(self.attack_card.rank)
        best_index = None
        best_defender_strength = -1

        # Special case: If computer has a 6 and can attack an Ace
        if self.attack_card.rank == '6':
            for i, defender_card in enumerate(self.defender.active_cards):
                if defender_card.card_state == CardState.BEATEN:
                    continue
                    
                if i == 0 and any(
                    j < len(self.defender.active_cards) and
                    self.defender.active_cards[j].card_state != CardState.BEATEN
                    for j in [1, 2, 3]
                ):
                    continue
                    
                if defender_card.rank == 'A':
                    return i

        # Special case: If computer has an Ace, it can beat anything except 6
        if self.attack_card.rank == 'A':
            for i, defender_card in enumerate(self.defender.active_cards):
                if defender_card.card_state == CardState.BEATEN or defender_card.rank == '6':
                    continue
                    
                if i == 0 and any(
                    j < len(self.defender.active_cards) and
                    self.defender.active_cards[j].card_state != CardState.BEATEN
                    for j in [1, 2, 3]
                ):
                    continue
                
                # Prioritize higher value cards
                defender_strength = self.CARD_RANKS.index(defender_card.rank)
                if defender_strength > best_defender_strength:
                    best_defender_strength = defender_strength
                    best_index = i
            
            if best_index is not None:
                return best_index

        # Normal case for other cards
        for i, defender_card in enumerate(self.defender.active_cards):
            if defender_card.card_state == CardState.BEATEN:
                continue

            if i == 0 and any(
                j < len(self.defender.active_cards) and
                self.defender.active_cards[j].card_state != CardState.BEATEN
                for j in [1, 2, 3]
            ):
                continue

            defender_strength = self.CARD_RANKS.index(defender_card.rank)
            
            # Check special case: if defender has Ace, computer can only beat it with 6
            if defender_card.rank == 'A' and self.attack_card.rank != '6':
                continue

            # The goal of computer algorithm is to find and beat the highest possible card
            if attacker_strength > defender_strength:
                if defender_strength > best_defender_strength:
                    best_defender_strength = defender_strength
                    best_index = i

        # If no beatable cards, consider draw
        if best_index is None:
            for i, defender_card in enumerate(self.defender.active_cards):
                if defender_card.card_state == CardState.BEATEN:
                    continue
                if i == 0 and any(
                    j < len(self.defender.active_cards) and
                    self.defender.active_cards[j].card_state != CardState.BEATEN
                    for j in [1, 2, 3]
                ):
                    continue
                if self.CARD_RANKS.index(defender_card.rank) == attacker_strength:
                    return i

        return "" if best_index is None else best_index
    
    # Used incase there is no way to attack or you want to skip move
    def attack_end(self):
        self.defender.deck.append(copy.copy(self.attack_card))
    
    def _draw_handle(self, defender_card: Card):
        self.draw_pile = []
        self.draw_pile = [self.attack_card, copy.copy(defender_card)]
        
        if defender_card in self.defender.active_cards:
            defender_card.card_state = CardState.BEATEN
        
        while True:
            if not self.attacker.deck:
                print(f"{self.defender.name} wins the draw (attacker out of cards)")
                self.defender.deck.extend(self.draw_pile)
                self.last_draw_winner = self.defender.name
                self.last_draw_cards = self.draw_pile
                break
            if not self.defender.deck:
                print(f"{self.attacker.name} wins the draw (defender out of cards)")
                self.attacker.deck.extend(self.draw_pile)
                self.last_draw_winner = self.attacker.name
                self.last_draw_cards = self.draw_pile
                break
            
            attacker_draw = self.attacker.deck.pop(0)
            defender_draw = self.defender.deck.pop(0)
            
            self.draw_pile.append(attacker_draw)
            self.draw_pile.append(defender_draw)
            
            # Special case for Ace vs 6
            if attacker_draw.rank == 'A' and defender_draw.rank == '6':
                print(f"DEBUG: {self.defender.name} wins draw! (6 beats Ace)")
                # Keep the attacker's card on the field
                self.attack_card = attacker_draw
                # Remove the attacker's card from the draw pile
                self.draw_pile.remove(attacker_draw)
                self.defender.deck.extend(self.draw_pile)
                self.last_draw_winner = self.defender.name
                self.last_draw_cards = self.draw_pile
                break
            elif attacker_draw.rank == '6' and defender_draw.rank == 'A':
                print(f"DEBUG: {self.attacker.name} wins draw! (6 beats Ace)")
                self.battle_cards.extend(self.draw_pile)
                self.last_draw_winner = self.attacker.name
                self.last_draw_cards = self.draw_pile
                self._check_goal_condition()
                break
            elif attacker_draw.rank == 'A' and defender_draw.rank != '6':
                print(f"DEBUG: {self.attacker.name} wins draw! (Ace beats {defender_draw.rank})")
                self.battle_cards.extend(self.draw_pile)
                self.last_draw_winner = self.attacker.name
                self.last_draw_cards = self.draw_pile
                self._check_goal_condition()
                break
            elif attacker_draw.rank != '6' and defender_draw.rank == 'A':
                print(f"DEBUG: {self.defender.name} wins draw! (Ace beats {attacker_draw.rank})")
                # Keep the attacker's card on the field
                self.attack_card = attacker_draw
                # Remove the attacker's card from the draw pile
                self.draw_pile.remove(attacker_draw)
                self.defender.deck.extend(self.draw_pile)
                self.last_draw_winner = self.defender.name
                self.last_draw_cards = self.draw_pile
                break
            elif attacker_draw.rank == 'A' and defender_draw.rank == 'A':
                print(f"DEBUG: Ace vs Ace draw! Drawing again...")
                continue
            
            # Normal comparison
            attacker_value = self.CARD_RANKS.index(attacker_draw.rank)
            defender_value = self.CARD_RANKS.index(defender_draw.rank)

            if attacker_value > defender_value:
                print("DEBUG: " + self.attacker.name + " wins draw!")
                self.battle_cards.extend(self.draw_pile)
                self.last_draw_winner = self.attacker.name
                self.last_draw_cards = self.draw_pile
                self._check_goal_condition()
                break
            if defender_value > attacker_value:
                print("DEBUG: " + self.defender.name + " wins draw!")
                # Keep the attacker's card on the field
                self.attack_card = attacker_draw
                # Remove the attacker's card from the draw pile
                self.draw_pile.remove(attacker_draw)
                self.defender.deck.extend(self.draw_pile)
                self.last_draw_winner = self.defender.name
                self.last_draw_cards = self.draw_pile
                break
    
    def _check_win_condition(self):
        if self.attacker.goals == 3 or self.defender.goals == 3 or len(self.attacker.deck) == 0 or len(self.defender.deck) == 0:
            self.game_running = False
            return True
        return False
    
    def _harder_computer_attack(self):
        # Does same thing as original except it now simulates draws and gauges possible gains 
        # Uncomment print statements to see how it works

        print("Computer thinks...")
        time.sleep(1)
        if not self.attack_card:
            return None
        attacker_strength = self.CARD_RANKS.index(self.attack_card.rank)
        best_index = None
        attack_score = float("-inf")
        self.position_bonus = {0:100} # Prefer GK over defenders
        # TODO: If you want to try, you could create a Graph that leads to beating GK 
        self.rank_bonus = {
            'A': 50,
            'K': 40,            # Prefer high rank cards over normal cards
            'Q': 30,
            'J': 20
        }

        # Special case: If computer has a 6 and can attack an Ace
        if self.attack_card.rank == '6':
            for i, defender_card in enumerate(self.defender.active_cards):
                if defender_card.card_state == CardState.BEATEN:
                    continue
                    
                if i == 0 and any(
                    j < len(self.defender.active_cards) and
                    self.defender.active_cards[j].card_state != CardState.BEATEN
                    for j in [1, 2, 3]
                ):
                    continue
                    
                if defender_card.rank == 'A':
                    return i

        for i, defender_card in enumerate(self.defender.active_cards):
            if defender_card.card_state == CardState.BEATEN:
                continue
            if i == 0 and any(
                j < len(self.defender.active_cards) and
                self.defender.active_cards[j].card_state != CardState.BEATEN
                for j in [1, 2, 3]
            ):
                continue
            defender_strength = self.CARD_RANKS.index(defender_card.rank)
           

            # Special case for Ace
            if self.attack_card.rank == 'A':
                if defender_card.rank == '6':
                    base_score = -1  # Ace loses to 6
                else:
                    base_score = 5   # Ace beats everything else
            elif defender_card.rank == 'A':
                if self.attack_card.rank == '6':
                    base_score = 5   # 6 beats Ace
                else:
                    base_score = -1  # Everything else loses to Ace
            # Normal cases
            elif attacker_strength > defender_strength:
                base_score = 5
            elif attacker_strength == defender_strength:
                base_score = 3
                simulation_score = self._simulate_draws(defender_card)
                base_score = base_score + simulation_score
                
            else:
                base_score = -1
            
            # Only adds position and rank bonus on winning moves
            if base_score > 0:
                bonus_score = self.position_bonus.get(i, 0) \
                            + self.rank_bonus.get(defender_card.rank, 0)
            
            else:
                bonus_score = 0

            total = base_score + bonus_score
            

            if total > attack_score:
                attack_score = total
                best_index = i

        if attack_score == -1: # If all moves lead to losing, skip turn
            return ""
        return best_index

    def _simulate_draws(self, defender_card):
        
        # Copies so that the current cards are not altered
        self.attacker_deck_sim = [copy.copy(card) for card in self.attacker.deck] 
        self.defender_deck_sim = [copy.copy(card) for card in self.defender.deck]
        self.draw_pile_sim = []
        self.draw_pile_sim = [copy.copy(self.attack_card), copy.copy(defender_card)]

        for i, card in enumerate(self.defender_deck_sim):
            if card.rank == defender_card.rank and card.suit == defender_card.suit:
                self.defender_deck_sim.pop(i)
        
            while True:
                if not self.attacker_deck_sim:
                    return len(self.draw_pile_sim)
                    
                if not self.defender_deck_sim:
                    return -len(self.draw_pile_sim)            
                
                attacker_draw = self.attacker_deck_sim.pop(0)
                defender_draw = self.defender_deck_sim.pop(0)
                
                self.draw_pile_sim.append(attacker_draw)
                self.draw_pile_sim.append(defender_draw)
                
                # Special case for Ace vs 6
                if attacker_draw.rank == 'A' and defender_draw.rank == '6':
                    return -len(self.draw_pile_sim)  # Defender wins
                elif attacker_draw.rank == '6' and defender_draw.rank == 'A':
                    return len(self.draw_pile_sim)   # Attacker wins
                elif attacker_draw.rank == 'A' and defender_draw.rank != '6':
                    return len(self.draw_pile_sim)   # Attacker wins
                elif attacker_draw.rank != '6' and defender_draw.rank == 'A':
                    return -len(self.draw_pile_sim)  # Defender wins
                
                # Normal comparison
                attacker_value = self.CARD_RANKS.index(attacker_draw.rank)
                defender_value = self.CARD_RANKS.index(defender_draw.rank)
                

                if attacker_value > defender_value:
                    return len(self.draw_pile_sim)
                
                if defender_value > attacker_value:
                    return -len(self.draw_pile_sim)

    def get_last_draw_info(self):
        """Return information about the last draw"""
        if not self.last_draw_cards:
            return None
            
        return {
            'cards': self.last_draw_cards,
            'winner': self.last_draw_winner
        }
    
        
    