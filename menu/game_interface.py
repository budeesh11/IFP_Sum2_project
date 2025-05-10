import pygame
import sys
import os
import random
import sys
import os

# Add parent directory to path to import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from player import Player
from deck import Deck
from card import Card
from card_state import CardState
from game_engine import GameEngine

class GameInterface:
    def __init__(self, game):
        self.game = game
        self.DISPLAY_W, self.DISPLAY_H = game.DISPLAY_W, game.DISPLAY_H
        self.display = game.display
        self.window = game.window
        
        # Game state
        self.running = True
        self.CARD_SUITS = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        self.CARD_RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        
        # Initialize deck and players
        self.initialize_game()
        
        # UI elements - smaller cards with more spacing
        self.card_width = 80
        self.card_height = 120
        self.card_spacing = 70
        self.selected_card_index = None
        self.message = ""
        self.message_timer = 0
        
        # Load card images
        self.card_images = {}
        self.card_back = None
        self.load_card_images()
    
    def initialize_game(self):
        # Create a deck
        deck = Deck(self.CARD_SUITS, self.CARD_RANKS)
        
        # Split the deck between players
        half_deck = len(deck.cards) // 2
        player_cards = deck.cards[:half_deck]
        computer_cards = deck.cards[half_deck:]
        
        # Create players or reset existing ones
        if hasattr(self, 'player') and hasattr(self, 'computer'):
            # Reset existing players
            self.player.deck = player_cards
            self.player.active_cards = []
            self.player.goals = 0
            
            self.computer.deck = computer_cards
            self.computer.active_cards = []
            self.computer.goals = 0
        else:
            # Create new players
            self.player = Player("Player", player_cards)
            self.computer = Player("Computer", computer_cards)
        
        # Initialize game engine
        self.engine = GameEngine(self.player, self.computer, self.CARD_SUITS, self.CARD_RANKS)
        
        # Make player the attacker (start first)
        self.engine.attacker = self.player
        self.engine.defender = self.computer
        
        # Draw initial active cards
        self.player.draw_active_cards()
        self.computer.draw_active_cards()
        
        # Set initial attack card
        self.engine.attack_card = self.engine.attacker.deck.pop(0)
        
        # Reset UI state
        self.selected_card_index = None
        self.message = ""
        self.message_timer = 0
        
        # Reset game state
        self.running = True
    
    def load_card_images(self):
        # Try to load card images from Cards folder
        try:
            # Load card back
            self.card_back = pygame.image.load("menu/Cards/Back_Blue.png")
            self.card_back = pygame.transform.scale(self.card_back, (self.card_width, self.card_height))
            
            # Map suit first letter to full name for file naming
            suit_map = {'H': 'Hearts', 'D': 'Diamonds', 'C': 'Clubs', 'S': 'Spades'}
            
            # Load card fronts
            for suit in self.CARD_SUITS:
                suit_letter = suit[0]  # First letter of the suit (H, D, C, S)
                for rank in self.CARD_RANKS:
                    card_key = f"{suit_letter}{rank}"
                    try:
                        # Card files are named like "HA.png" for Hearts Ace, "C10.png" for Clubs 10
                        image_path = f"menu/Cards/{card_key}.png"
                        if os.path.exists(image_path):
                            image = pygame.image.load(image_path)
                            self.card_images[card_key] = pygame.transform.scale(image, (self.card_width, self.card_height))
                        else:
                            # Create a default card if image doesn't exist
                            self.create_default_card(suit, rank)
                    except Exception as e:
                        print(f"Error loading card image {card_key}: {e}")
                        # Create a default card if loading fails
                        self.create_default_card(suit, rank)
        except Exception as e:
            print(f"Error loading card images: {e}")
            # Create default cards if loading fails
            for suit in self.CARD_SUITS:
                for rank in self.CARD_RANKS:
                    self.create_default_card(suit, rank)
    
    def create_default_card(self, suit, rank):
        card_key = f"{suit[0]}{rank}"
        card_surface = pygame.Surface((self.card_width, self.card_height))
        card_surface.fill((255, 255, 255))  # White background
        
        # Draw border
        pygame.draw.rect(card_surface, (0, 0, 0), (0, 0, self.card_width, self.card_height), 2)
        
        # Draw suit symbol and rank
        font = pygame.font.Font(None, 30)
        
        # Set color based on suit
        color = (255, 0, 0) if suit in ['Hearts', 'Diamonds'] else (0, 0, 0)
        
        # Draw rank
        rank_text = font.render(rank, True, color)
        card_surface.blit(rank_text, (5, 5))
        
        # Draw suit
        suit_symbol = '♥' if suit == 'Hearts' else '♦' if suit == 'Diamonds' else '♣' if suit == 'Clubs' else '♠'
        suit_text = font.render(suit_symbol, True, color)
        card_surface.blit(suit_text, (5, 25))
        
        # Draw center symbol
        center_text = font.render(f"{rank}{suit_symbol}", True, color)
        card_surface.blit(center_text, (self.card_width // 2 - center_text.get_width() // 2, 
                                       self.card_height // 2 - center_text.get_height() // 2))
        
        self.card_images[card_key] = card_surface
    
    def draw_card(self, card, x, y, is_beaten=False, is_selected=False, is_goalkeeper=False):
        if card is None:
            return
        
        card_key = f"{card.suit[0]}{card.rank}"
        
        # Get card image
        card_image = self.card_images.get(card_key, self.card_back)
        
        # Draw card with appropriate visual state
        if is_beaten:
            # Draw a grayed-out version for beaten cards
            gray_card = card_image.copy()
            overlay = pygame.Surface((self.card_width, self.card_height), pygame.SRCALPHA)
            overlay.fill((128, 128, 128, 128))
            gray_card.blit(overlay, (0, 0))
            self.display.blit(gray_card, (x, y))
        else:
            self.display.blit(card_image, (x, y))
        
        # Draw selection indicator
        if is_selected:
            pygame.draw.rect(self.display, (255, 255, 0), (x-2, y-2, self.card_width+4, self.card_height+4), 3)
        
        # Draw goalkeeper indicator
        if is_goalkeeper:
            pygame.draw.rect(self.display, (255, 0, 0), (x-2, y-2, self.card_width+4, self.card_height+4), 2)
            font = pygame.font.Font(None, 24)
            gk_text = font.render("GK", True, (255, 0, 0))
            self.display.blit(gk_text, (x + self.card_width // 2 - gk_text.get_width() // 2, y - 20))
    
    def draw_game_state(self):
        # Clear screen with field background
        self.display.blit(self.game.field_image, (0, 0))
        
        # Draw scores
        font = pygame.font.Font(None, 36)
        player_score_text = font.render(f"Player: {self.player.goals} goals", True, (255, 255, 255))
        computer_score_text = font.render(f"Computer: {self.computer.goals} goals", True, (255, 255, 255))
        self.display.blit(player_score_text, (20, 20))
        self.display.blit(computer_score_text, (self.DISPLAY_W - computer_score_text.get_width() - 20, 20))
        
        # Draw deck counts
        player_deck_text = font.render(f"Cards: {len(self.player.deck)}", True, (255, 255, 255))
        computer_deck_text = font.render(f"Cards: {len(self.computer.deck)}", True, (255, 255, 255))
        self.display.blit(player_deck_text, (20, self.DISPLAY_H - 40))
        self.display.blit(computer_deck_text, (self.DISPLAY_W - computer_deck_text.get_width() - 20, 80))
        
        # Draw current attacker/defender status
        turn_text = font.render(f"{'Player' if self.engine.attacker == self.player else 'Computer'} is attacking", True, (255, 255, 0))
        self.display.blit(turn_text, (self.DISPLAY_W // 2 - turn_text.get_width() // 2, 20))
        
        # Calculate vertical positions with much more space
        # Computer cards moved much higher up
        computer_gk_y = 30
        computer_defenders_y = computer_gk_y + self.card_height + 30
        
        # Attack card in the middle with clear space
        attack_card_y = self.DISPLAY_H // 2 - self.card_height // 2
        
        # Player cards moved much lower down
        player_defenders_y = self.DISPLAY_H - self.card_height * 2 - 80
        player_gk_y = self.DISPLAY_H - self.card_height - 20
        
        # Draw attack card with highlight
        attack_x = self.DISPLAY_W // 2 - self.card_width // 2
        if self.engine.attack_card:
            # Draw highlight behind the attack card
            highlight_rect = pygame.Rect(attack_x - 5, attack_card_y - 5, 
                                       self.card_width + 10, self.card_height + 10)
            pygame.draw.rect(self.display, (255, 215, 0, 150), highlight_rect, border_radius=5)
            
            self.draw_card(self.engine.attack_card, attack_x, attack_card_y)
            attack_text = font.render("Attack Card", True, (255, 255, 255))
            self.display.blit(attack_text, (attack_x + self.card_width // 2 - attack_text.get_width() // 2, 
                                          attack_card_y - 30))
        
        # Draw computer's active cards in the football formation (1 GK, 3 defenders)
        # Goalkeeper
        if len(self.computer.active_cards) > 0:
            gk_x = self.DISPLAY_W // 2 - self.card_width // 2
            is_beaten = self.computer.active_cards[0].card_state == CardState.BEATEN
            self.draw_card(self.computer.active_cards[0], gk_x, computer_gk_y, is_beaten, False, True)
        
        # Draw "Goalkeeper" text
        gk_label = font.render("Goalkeeper", True, (255, 255, 255))
        self.display.blit(gk_label, (self.DISPLAY_W // 2 - gk_label.get_width() // 2, computer_gk_y - 20))
        
        # Defenders (3 cards in a row)
        total_width = (min(3, len(self.computer.active_cards) - 1) - 1) * (self.card_width + self.card_spacing) + self.card_width
        defenders_start_x = self.DISPLAY_W // 2 - total_width // 2
        
        for i in range(1, min(4, len(self.computer.active_cards))):
            card_x = defenders_start_x + (i - 1) * (self.card_width + self.card_spacing)
            is_beaten = self.computer.active_cards[i].card_state == CardState.BEATEN
            self.draw_card(self.computer.active_cards[i], card_x, computer_defenders_y, is_beaten)
        
        # Draw player's active cards in the football formation (1 GK, 3 defenders)
        # Defenders (3 cards in a row)
        total_width = (min(3, len(self.player.active_cards) - 1) - 1) * (self.card_width + self.card_spacing) + self.card_width
        defenders_start_x = self.DISPLAY_W // 2 - total_width // 2
        
        for i in range(1, min(4, len(self.player.active_cards))):
            card_x = defenders_start_x + (i - 1) * (self.card_width + self.card_spacing)
            is_beaten = self.player.active_cards[i].card_state == CardState.BEATEN
            is_selected = i == self.selected_card_index
            self.draw_card(self.player.active_cards[i], card_x, player_defenders_y, is_beaten, is_selected)
        
        # Goalkeeper
        if len(self.player.active_cards) > 0:
            gk_x = self.DISPLAY_W // 2 - self.card_width // 2
            is_beaten = self.player.active_cards[0].card_state == CardState.BEATEN
            is_selected = 0 == self.selected_card_index
            self.draw_card(self.player.active_cards[0], gk_x, player_gk_y, is_beaten, is_selected, True)
        
        # Draw "Goalkeeper" text
        gk_label = font.render("Goalkeeper", True, (255, 255, 255))
        self.display.blit(gk_label, (self.DISPLAY_W // 2 - gk_label.get_width() // 2, player_gk_y + self.card_height + 10))
        
        # Draw message if there is one
        if self.message and self.message_timer > 0:
            message_font = pygame.font.Font(None, 42)
            message_text = message_font.render(self.message, True, (255, 255, 255))
            message_x = self.DISPLAY_W // 2 - message_text.get_width() // 2
            message_y = attack_card_y + self.card_height + 30
            
            # Draw background for better readability
            bg_rect = message_text.get_rect(center=(self.DISPLAY_W // 2, message_y + message_text.get_height() // 2))
            bg_rect.inflate_ip(20, 10)
            pygame.draw.rect(self.display, (0, 0, 0, 128), bg_rect, border_radius=5)
            
            self.display.blit(message_text, (message_x, message_y))
            self.message_timer -= 1
    
    def show_message(self, message, duration=120):
        self.message = message
        self.message_timer = duration
    
    def show_card_battle_result(self, attacker_card, defender_card, result):
        """Show a visual comparison of the attacking and defending cards with the result"""
        # Store the current state to restore later
        original_message = self.message
        original_timer = self.message_timer
        
        # Center position for displaying cards
        center_x = self.DISPLAY_W // 2
        center_y = self.DISPLAY_H // 2
        card_spacing = 80  # Space between the two cards
        
        # Draw the background and game state
        self.display.blit(self.game.field_image, (0, 0))
        
        # Add semi-transparent overlay for better visibility
        overlay = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))  # Dark semi-transparent overlay
        self.display.blit(overlay, (0, 0))
        
        # Draw the cards side by side
        left_card_x = center_x - self.card_width - card_spacing // 2
        right_card_x = center_x + card_spacing // 2
        
        # Draw attacker's card
        self.draw_card(attacker_card, left_card_x, center_y - self.card_height // 2)
        
        # Draw defender's card
        self.draw_card(defender_card, right_card_x, center_y - self.card_height // 2)
        
        # Draw labels for the cards
        font = pygame.font.Font(None, 24)
        attacker_name = self.engine.attacker.name
        defender_name = self.engine.defender.name
        
        attacker_label = font.render(f"{attacker_name}'s card", True, (255, 255, 0))
        defender_label = font.render(f"{defender_name}'s card", True, (0, 255, 255))
        
        self.display.blit(attacker_label, (left_card_x + self.card_width // 2 - attacker_label.get_width() // 2, 
                                         center_y - self.card_height // 2 - 30))
        self.display.blit(defender_label, (right_card_x + self.card_width // 2 - defender_label.get_width() // 2, 
                                         center_y - self.card_height // 2 - 30))
        
        # Draw result based on the outcome
        result_font = pygame.font.Font(None, 48)
        vs_text = result_font.render("VS", True, (255, 255, 255))
        self.display.blit(vs_text, (center_x - vs_text.get_width() // 2, center_y - vs_text.get_height() // 2))
        
        if result == "Success":
            # Draw winning indicator for attacker
            pygame.draw.rect(self.display, (0, 255, 0), 
                           (left_card_x - 5, center_y - self.card_height // 2 - 5, 
                            self.card_width + 10, self.card_height + 10), 3)
            
            # Draw X over defender's card
            pygame.draw.line(self.display, (255, 0, 0), 
                           (right_card_x, center_y - self.card_height // 2),
                           (right_card_x + self.card_width, center_y + self.card_height // 2), 4)
            pygame.draw.line(self.display, (255, 0, 0), 
                           (right_card_x + self.card_width, center_y - self.card_height // 2),
                           (right_card_x, center_y + self.card_height // 2), 4)
            
            result_text = result_font.render(f"{attacker_name} wins!", True, (0, 255, 0))
        elif result == "Fail":
            # Draw winning indicator for defender
            pygame.draw.rect(self.display, (0, 255, 0), 
                           (right_card_x - 5, center_y - self.card_height // 2 - 5, 
                            self.card_width + 10, self.card_height + 10), 3)
            
            # Draw X over attacker's card
            pygame.draw.line(self.display, (255, 0, 0), 
                           (left_card_x, center_y - self.card_height // 2),
                           (left_card_x + self.card_width, center_y + self.card_height // 2), 4)
            pygame.draw.line(self.display, (255, 0, 0), 
                           (left_card_x + self.card_width, center_y - self.card_height // 2),
                           (left_card_x, center_y + self.card_height // 2), 4)
            
            result_text = result_font.render(f"{defender_name} wins!", True, (0, 255, 0))
        else:
            # Draw draw indicator
            result_text = result_font.render("Draw!", True, (255, 255, 0))
        
        # Display the result text
        self.display.blit(result_text, (center_x - result_text.get_width() // 2, center_y + self.card_height // 2 + 20))
        
        # Display card ranks
        attacker_rank = font.render(f"Rank: {attacker_card.rank}", True, (255, 255, 255))
        defender_rank = font.render(f"Rank: {defender_card.rank}", True, (255, 255, 255))
        
        self.display.blit(attacker_rank, (left_card_x + self.card_width // 2 - attacker_rank.get_width() // 2, 
                                        center_y + self.card_height // 2 + 60))
        self.display.blit(defender_rank, (right_card_x + self.card_width // 2 - defender_rank.get_width() // 2, 
                                        center_y + self.card_height // 2 + 60))
        
        # Update the display
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()
        pygame.time.delay(2000)  # 2 second delay
        
        # Restore original message
        self.message = original_message
        self.message_timer = original_timer

    def handle_player_attack(self, target_index):
        if self.engine.attacker != self.player:
            self.show_message("It's not your turn to attack!")
            return
        
        # Store the target card for visualization
        try:
            target_card = self.computer.active_cards[target_index]
        except:
            return
        
        result = self.engine.attack_handle(target_index)
        
        if result == "Success":
            self.show_message("Attack successful!")
            
            # Show the card battle visualization
            self.show_card_battle_result(self.engine.attack_card, target_card, result)
            
            # Check if a goal was scored (all defender cards beaten)
            all_beaten = True
            for card in self.computer.active_cards:
                if card.card_state != CardState.BEATEN:
                    all_beaten = False
                    break
            
            if all_beaten:
                # Don't increment here as the engine already does it FIXED: error that would occur when a goal is scored and score is incremented twice
                self.show_message(f"GOAL! You scored! Score: {self.player.goals}-{self.computer.goals}")
            
            if self._check_game_over():
                return
            
            if not self.engine.valid_for_next_attack():
                self.engine.change_turn()
                self.show_message("Computer's turn")
        elif result == "Draw":
            self.show_message("Draw! Cards will be compared...")
            self.handle_draw_visualization()
            
            if self._check_game_over():
                return
            
            # Check who won the draw
            draw_info = self.engine.get_last_draw_info()
            if draw_info and draw_info['winner'] == self.computer.name:
                # If player lost the draw, change turn to computer
                self.engine.change_turn()
                self.show_message("You lost the draw. Computer's turn now.")
            else:
                # If player won the draw, keep player's turn
                self.show_message("You won the draw. Your turn continues.")
                if not self.engine.valid_for_next_attack():
                    self.engine.change_turn()
                    self.show_message("Computer's turn")
        elif result == "Fail":
            self.show_message("Attack failed!")
            
            # Show the card battle visualization
            self.show_card_battle_result(self.engine.attack_card, target_card, result)
            
            self.engine.change_turn()
            self.show_message("Computer's turn")
        else:
            self.show_message(result)  # Show any other message/error
    
    def handle_computer_turn(self):
        if self.engine.attacker != self.computer:
            return
        
        # Simulate thinking (delay between computer's moves)
        pygame.time.delay(1000)
        
        # Get computer's attack choice
        target_index = self.engine.computer_attack()
        
        if target_index == "":
            self.show_message("Computer ends its turn")
            self.engine.attack_end()
            self.engine.change_turn()
            return
        
        # Store the target card for visualization
        try:
            target_card = self.player.active_cards[target_index]
        except:
            return
        
        # Execute attack
        result = self.engine.attack_handle(target_index)
        
        if result == "Success":
            self.show_message("Computer's attack was successful!")
            
            # Show the card battle visualization
            self.show_card_battle_result(self.engine.attack_card, target_card, result)
            
            # Check if a goal was scored (all defender cards beaten)
            all_beaten = True
            for card in self.player.active_cards:
                if card.card_state != CardState.BEATEN:
                    all_beaten = False
                    break
            
            if all_beaten:
                # Don't increment here as the engine already does it (same as line 423)
                self.show_message(f"GOAL! Computer scored! Score: {self.player.goals}-{self.computer.goals}")
            
            if self._check_game_over():
                return
            
            if not self.engine.valid_for_next_attack():
                self.engine.change_turn()
        elif result == "Draw":
            self.show_message("Draw! Cards will be compared...")
            self.handle_draw_visualization()
            
            if self._check_game_over():
                return
            
            # Check who won the draw
            draw_info = self.engine.get_last_draw_info()
            if draw_info and draw_info['winner'] == self.player.name:
                # If computer lost the draw, change turn to player
                self.engine.change_turn()
                self.show_message("Computer lost the draw. Your turn now.")
            else:
                # If computer won the draw, keep computer's turn
                self.show_message("Computer won the draw. Computer's turn continues.")
                if not self.engine.valid_for_next_attack():
                    self.engine.change_turn()
        elif result == "Fail":
            self.show_message("Computer's attack failed!")
            
            # Show the card battle visualization
            self.show_card_battle_result(self.engine.attack_card, target_card, result)
            
            self.engine.change_turn()
    
    def handle_draw_visualization(self):
        """Visualize the draw process with intervals between each step"""
        #store the current state to restore later
        original_message = self.message
        original_timer = self.message_timer
        
        # Get draw information from the engine
        draw_info = self.engine.get_last_draw_info()
        if not draw_info:
            self.show_message("No draw information available")
            return
        
        attacker_name = self.engine.attacker.name
        defender_name = self.engine.defender.name
        draw_cards = draw_info['cards']
        winner = draw_info['winner']
        
        # Center position for displaying cards
        center_x = self.DISPLAY_W // 2
        center_y = self.DISPLAY_H // 2
        card_spacing = 60  # Increased space between the two cards in each pair
        
        # Show initial cards that caused the draw
        self.show_message(f"Draw! {attacker_name}'s {draw_cards[0].rank}{draw_cards[0].suit[0]} vs {defender_name}'s {draw_cards[1].rank}{draw_cards[1].suit[0]}")
        
        # Draw the background and game state
        self.display.blit(self.game.field_image, (0, 0))
        
        # Add semi-transparent overlay for better visibility (during the draw visualization scenes)
        overlay = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 120))  # Dark semi-transparent overlay
        self.display.blit(overlay, (0, 0))
        
        # Draw the initial pair of cards in the center with more space between them
        left_card_x = center_x - self.card_width - card_spacing // 2
        right_card_x = center_x + card_spacing // 2
        
        # Draw attacker's card
        self.draw_card(draw_cards[0], left_card_x, center_y - self.card_height // 2)
        
        # Draw defender's card
        self.draw_card(draw_cards[1], right_card_x, center_y - self.card_height // 2)
        
        # Draw labels for the cards with different colors and better positioning
        font = pygame.font.Font(None, 24)
        
        # Attacker label (positioned above the card)
        attacker_label = font.render(f"{attacker_name}'s card", True, (255, 255, 0))
        self.display.blit(attacker_label, (left_card_x + self.card_width // 2 - attacker_label.get_width() // 2, 
                                         center_y - self.card_height // 2 - 30))
        
        # Defender label (positioned above the card)
        defender_label = font.render(f"{defender_name}'s card", True, (0, 255, 255))
        self.display.blit(defender_label, (right_card_x + self.card_width // 2 - defender_label.get_width() // 2, 
                                         center_y - self.card_height // 2 - 30))
        
        # Draw message at the top
        message_font = pygame.font.Font(None, 36)
        message_text = message_font.render(self.message, True, (255, 255, 255))
        self.display.blit(message_text, (center_x - message_text.get_width() // 2, 50))
        
        # Update the display
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()
        pygame.time.delay(2000)  # 2 second delay
        
        # Show each pair of cards drawn in the draw battle
        for i in range(2, len(draw_cards), 2):
            if i+1 < len(draw_cards):
                self.show_message(f"Draw continues! {attacker_name} draws {draw_cards[i].rank}{draw_cards[i].suit[0]}, {defender_name} draws {draw_cards[i+1].rank}{draw_cards[i+1].suit[0]}")
                
                # Redraw the background and overlay
                self.display.blit(self.game.field_image, (0, 0))
                self.display.blit(overlay, (0, 0))
                
                # Draw the new pair of cards
                self.draw_card(draw_cards[i], left_card_x, center_y - self.card_height // 2)
                self.draw_card(draw_cards[i+1], right_card_x, center_y - self.card_height // 2)
                
                # Draw labels for the cards with different colors and better positioning
                self.display.blit(attacker_label, (left_card_x + self.card_width // 2 - attacker_label.get_width() // 2, 
                                               center_y - self.card_height // 2 - 30))
                self.display.blit(defender_label, (right_card_x + self.card_width // 2 - defender_label.get_width() // 2, 
                                               center_y - self.card_height // 2 - 30))
                
                # Draw the draw count
                draw_count = i // 2 + 1
                count_text = message_font.render(f"Draw #{draw_count}", True, (255, 255, 0))
                self.display.blit(count_text, (center_x - count_text.get_width() // 2, 20))
                
                # Draw message
                message_text = message_font.render(self.message, True, (255, 255, 255))
                self.display.blit(message_text, (center_x - message_text.get_width() // 2, 50))
                
                # Draw the pile count
                pile_count = i + 2  # Number of cards in the draw pile so far
                pile_text = font.render(f"Cards in draw pile: {pile_count}", True, (255, 255, 255))
                self.display.blit(pile_text, (center_x - pile_text.get_width() // 2, center_y + self.card_height // 2 + 40))
                
                # Update the display
                self.game.window.blit(self.game.display, (0, 0))
                pygame.display.update()
                pygame.time.delay(2000)  # 2 second delay
        
        # Show the winner
        if winner:
            self.show_message(f"{winner} wins the draw! All cards go to {winner}'s deck.")
            
            # Redraw the background and overlay
            self.display.blit(self.game.field_image, (0, 0))
            self.display.blit(overlay, (0, 0))
            
            # Draw the last pair of cards
            last_attacker_card = draw_cards[-2] if len(draw_cards) >= 2 else draw_cards[0]
            last_defender_card = draw_cards[-1] if len(draw_cards) >= 2 else draw_cards[1]
            
            self.draw_card(last_attacker_card, left_card_x, center_y - self.card_height // 2)
            self.draw_card(last_defender_card, right_card_x, center_y - self.card_height // 2)
            
            # Draw labels for the cards with different colors and better positioning
            self.display.blit(attacker_label, (left_card_x + self.card_width // 2 - attacker_label.get_width() // 2, 
                                           center_y - self.card_height // 2 - 30))
            self.display.blit(defender_label, (right_card_x + self.card_width // 2 - defender_label.get_width() // 2, 
                                           center_y - self.card_height // 2 - 30))
            
            # Highlight the winner's card with a glowing effect
            winner_card_x = left_card_x if winner == attacker_name else right_card_x
            glow_size = 10
            glow_rect = pygame.Rect(winner_card_x - glow_size, 
                                  center_y - self.card_height // 2 - glow_size,
                                  self.card_width + glow_size * 2, 
                                  self.card_height + glow_size * 2)
            pygame.draw.rect(self.display, (255, 215, 0, 150), glow_rect, border_radius=5)
            
            # Draw winner message
            winner_text = message_font.render(f"{winner} WINS THE DRAW!", True, (255, 215, 0))
            self.display.blit(winner_text, (center_x - winner_text.get_width() // 2, 20))
            
            # Draw message
            message_text = message_font.render(self.message, True, (255, 255, 255))
            self.display.blit(message_text, (center_x - message_text.get_width() // 2, 50))
            
            # Draw the pile count
            pile_count = len(draw_cards)
            pile_text = font.render(f"Total cards won: {pile_count}", True, (255, 255, 255))
            self.display.blit(pile_text, (center_x - pile_text.get_width() // 2, center_y + self.card_height // 2 + 40))
            
            # Update the display
            self.game.window.blit(self.game.display, (0, 0))
            pygame.display.update()
            pygame.time.delay(2000)  # 2 second delay
        
        # Restore original message
        self.message = original_message
        self.message_timer = original_timer
    
    def _check_game_over(self):
        if self.player.goals >= 3:
            self.show_message(f"You win! You scored 3 goals! Final score: {self.player.goals}-{self.computer.goals}")
            self.engine.game_running = False
            return True
        elif self.computer.goals >= 3:
            self.show_message(f"Computer wins! It scored 3 goals! Final score: {self.player.goals}-{self.computer.goals}")
            self.engine.game_running = False
            return True
        elif len(self.player.deck) == 0 and len(self.player.active_cards) == 0:
            self.show_message(f"You lose! You ran out of cards! Final score: {self.player.goals}-{self.computer.goals}")
            self.engine.game_running = False
            return True
        elif len(self.computer.deck) == 0 and len(self.computer.active_cards) == 0:
            self.show_message(f"You win! Computer ran out of cards! Final score: {self.player.goals}-{self.computer.goals}")
            self.engine.game_running = False
            return True
        return False
    
    def get_computer_card_at_position(self, mouse_pos):
        # Calculate vertical positions
        computer_gk_y = 30
        computer_defenders_y = computer_gk_y + self.card_height + 30
        
        # Check goalkeeper
        if len(self.computer.active_cards) > 0:
            gk_x = self.DISPLAY_W // 2 - self.card_width // 2
            gk_rect = pygame.Rect(gk_x, computer_gk_y, self.card_width, self.card_height)
            if gk_rect.collidepoint(mouse_pos):
                return 0
        
        # Check defenders
        total_width = (min(3, len(self.computer.active_cards) - 1) - 1) * (self.card_width + self.card_spacing) + self.card_width
        defenders_start_x = self.DISPLAY_W // 2 - total_width // 2
        
        for i in range(1, min(4, len(self.computer.active_cards))):
            card_x = defenders_start_x + (i - 1) * (self.card_width + self.card_spacing)
            card_rect = pygame.Rect(card_x, computer_defenders_y, self.card_width, self.card_height)
            if card_rect.collidepoint(mouse_pos):
                return i
        
        return None
    
    def get_player_card_at_position(self, mouse_pos):
        # Calculate vertical positions
        player_defenders_y = self.DISPLAY_H - self.card_height * 2 - 80
        player_gk_y = self.DISPLAY_H - self.card_height - 20
        
        # Check goalkeeper
        if len(self.player.active_cards) > 0:
            gk_x = self.DISPLAY_W // 2 - self.card_width // 2
            gk_rect = pygame.Rect(gk_x, player_gk_y, self.card_width, self.card_height)
            if gk_rect.collidepoint(mouse_pos):
                return 0
        
        # Check defenders
        total_width = (min(3, len(self.player.active_cards) - 1) - 1) * (self.card_width + self.card_spacing) + self.card_width
        defenders_start_x = self.DISPLAY_W // 2 - total_width // 2
        
        for i in range(1, min(4, len(self.player.active_cards))):
            card_x = defenders_start_x + (i - 1) * (self.card_width + self.card_spacing)
            card_rect = pygame.Rect(card_x, player_defenders_y, self.card_width, self.card_height)
            if card_rect.collidepoint(mouse_pos):
                return i
        
        return None
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.game.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.game.pause = True
                elif event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    # Select next/previous card
                    if not self.player.active_cards:
                        continue
                    
                    if self.selected_card_index is None:
                        self.selected_card_index = 0
                    else:
                        if event.key == pygame.K_LEFT:
                            self.selected_card_index = (self.selected_card_index - 1) % len(self.player.active_cards)
                        else:
                            self.selected_card_index = (self.selected_card_index + 1) % len(self.player.active_cards)
                elif event.key == pygame.K_RETURN:
                    # If it's player's turn to attack and a computer card is selected, attack it
                    if self.selected_card_index is not None and self.engine.attacker == self.player:
                        self.handle_player_attack(self.selected_card_index)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                
                # If it's player's turn to attack, check if they clicked on a computer card
                if self.engine.attacker == self.player:
                    target_index = self.get_computer_card_at_position(mouse_pos)
                    if target_index is not None:
                        self.handle_player_attack(target_index)
                
                # Check if player clicked on one of their own cards to select it
                player_card_index = self.get_player_card_at_position(mouse_pos)
                if player_card_index is not None:
                    self.selected_card_index = player_card_index
    
    def run(self):
        clock = pygame.time.Clock()
        
        while self.running and self.engine.game_running:
            if self.game.pause:
                self.game.show_pause_menu()
                continue
                
            self.handle_events()
            
            # Handle computer's turn
            if self.engine.attacker == self.computer and self.message_timer <= 0:
                self.handle_computer_turn()
            
            self.draw_game_state()
            
            self.game.window.blit(self.game.display, (0, 0))
            pygame.display.update()
            clock.tick(60)
        
        # Show game over screen
        self.show_game_over()
    
    def show_game_over(self):
        if not self.engine.game_running:
            font = pygame.font.Font(None, 72)
            if self.player.goals >= 3:
                result_text = "You Win!"
            elif self.computer.goals >= 3:
                result_text = "Computer Wins!"
            elif len(self.player.deck) == 0 and len(self.player.active_cards) == 0:
                result_text = "You Lose!"
            elif len(self.computer.deck) == 0 and len(self.computer.active_cards) == 0:
                result_text = "You Win!"
            else:
                result_text = "Game Over"
            
            text = font.render(result_text, True, (255, 255, 255))
            text_rect = text.get_rect(center=(self.DISPLAY_W // 2, self.DISPLAY_H // 2))
            
            # Instruction text
            small_font = pygame.font.Font(None, 36)
            instruction = small_font.render("Press BACKSPACE to return to menu", True, (255, 255, 255))
            instruction_rect = instruction.get_rect(center=(self.DISPLAY_W // 2, self.DISPLAY_H // 2 + 100))
            
            # Wait for user to press a key
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                        self.game.running = False
                        waiting = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_BACKSPACE:
                            self.game.playing = False
                            waiting = False
                
                # Draw game over screen
                self.display.blit(self.game.field_image, (0, 0))
                
                # Add semi-transparent overlay
                overlay = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 180))
                self.display.blit(overlay, (0, 0))
                
                # Draw text
                self.display.blit(text, text_rect)
                self.display.blit(instruction, instruction_rect)
                
                # Draw final score
                score_text = small_font.render(f"Final Score: Player {self.player.goals} - {self.computer.goals} Computer", True, (255, 255, 255))
                score_rect = score_text.get_rect(center=(self.DISPLAY_W // 2, self.DISPLAY_H // 2 + 50))
                self.display.blit(score_text, score_rect)
                
                self.game.window.blit(self.game.display, (0, 0))
                pygame.display.update() 