import pygame
import random
import sys
from typing import List, Tuple, Optional

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 700
CARD_WIDTH, CARD_HEIGHT = 100, 140
CARD_SPACING = 20
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 100, 0)
RED = (200, 0, 0)
BLUE = (0, 0, 200)
GRAY = (200, 200, 200)
FONT_SIZE = 24

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Football Card Game")
font = pygame.font.SysFont(None, FONT_SIZE)
clock = pygame.time.Clock()

class Card:
    def __init__(self, value: int):
        self.value = value
        self.rect = pygame.Rect(0, 0, CARD_WIDTH, CARD_HEIGHT)
        
    def draw(self, x: int, y: int, highlighted: bool = False):
        # Update card position
        self.rect.x, self.rect.y = x, y
        
        # Draw card
        color = WHITE
        border_color = BLUE if highlighted else BLACK
        border_width = 3 if highlighted else 1
        
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, border_color, self.rect, border_width)
        
        # Draw card value
        text = font.render(str(self.value), True, BLACK)
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)

class Player:
    def __init__(self, name: str):
        self.name = name
        self.deck: List[Card] = []
        self.team: List[Card] = []  # 3 defenders and 1 goalkeeper
        self.is_attacking = False
        self.goals = 0
        
    def draw_team(self, is_opponent: bool = False):
        y = 500 if not is_opponent else 100
        
        for i, card in enumerate(self.team):
            role = "GK" if i == 3 else f"DEF {i+1}"
            x = 250 + i * (CARD_WIDTH + CARD_SPACING)
            card.draw(x, y)
            
            # Draw role label
            label = font.render(role, True, BLACK)
            label_rect = label.get_rect(centerx=x + CARD_WIDTH//2, y=y-30 if not is_opponent else y+CARD_HEIGHT+10)
            screen.blit(label, label_rect)
    
    def draw_deck(self, x: int, y: int):
        if self.deck:
            # Draw deck with count
            pygame.draw.rect(screen, GRAY, (x, y, CARD_WIDTH, CARD_HEIGHT))
            pygame.draw.rect(screen, BLACK, (x, y, CARD_WIDTH, CARD_HEIGHT), 1)
            
            count_text = font.render(f"{len(self.deck)}", True, BLACK)
            count_rect = count_text.get_rect(center=(x + CARD_WIDTH//2, y + CARD_HEIGHT//2))
            screen.blit(count_text, count_rect)
            
            # Draw player name
            name_text = font.render(self.name, True, BLACK)
            name_rect = name_text.get_rect(centerx=x + CARD_WIDTH//2, y=y-30)
            screen.blit(name_text, name_rect)
            
            # Draw current score
            score_text = font.render(f"Goals: {self.goals}", True, BLACK)
            score_rect = score_text.get_rect(centerx=x + CARD_WIDTH//2, y=y+CARD_HEIGHT+10)
            screen.blit(score_text, score_rect)

class Game:
    def __init__(self):
        self.player1 = Player("Player 1")
        self.player2 = Player("Player 2")
        self.turn = 1  # 1 for player1, 2 for player2
        self.init_game()
        self.current_attack_card: Optional[Card] = None
        self.current_defense_index = 0
        self.attack_result = None  # None, "win", "lose"
        self.game_message = ""
        self.defense_index_beaten = []  # Indices of defense cards that have been beaten
        
    def init_game(self):
        # Create deck (1-10 values, 4 of each value)
        full_deck = [Card(value) for value in range(1, 11) for _ in range(4)]
        random.shuffle(full_deck)
        
        # Divide deck between players
        half = len(full_deck) // 2
        self.player1.deck = full_deck[:half]
        self.player2.deck = full_deck[half:]
        
        # Draw teams for both players
        self.draw_teams()
        
        # Set first player as attacker
        self.player1.is_attacking = True
        self.player2.is_attacking = False
    
    def draw_teams(self):
        # Draw 4 cards for each player's team (3 defenders + 1 goalkeeper)
        for _ in range(4):
            if self.player1.deck:
                self.player1.team.append(self.player1.deck.pop(0))
            if self.player2.deck:
                self.player2.team.append(self.player2.deck.pop(0))
    
    def get_attacking_player(self) -> Player:
        return self.player1 if self.player1.is_attacking else self.player2
    
    def get_defending_player(self) -> Player:
        return self.player2 if self.player1.is_attacking else self.player1
    
    def switch_turns(self):
        self.player1.is_attacking = not self.player1.is_attacking
        self.player2.is_attacking = not self.player2.is_attacking
        self.current_defense_index = 0
        self.defense_index_beaten = []
        self.game_message = f"{self.get_attacking_player().name} is now attacking"
    
    def draw_attack_card(self):
        attacking_player = self.get_attacking_player()
        
        # If attacker has no cards in deck, use defense cards
        if not attacking_player.deck and attacking_player.team:
            self.current_attack_card = attacking_player.team.pop(0)
            self.game_message = f"{attacking_player.name} is using a defense card to attack"
        elif attacking_player.deck:
            self.current_attack_card = attacking_player.deck.pop(0)
        else:
            # Game over - attacker has no cards left
            self.game_message = f"Game over! {self.get_defending_player().name} wins! (No cards left)"
            return False
        
        return True
    
    def compare_cards(self, attack_card: Card, defense_card: Card) -> bool:
        # Return True if attack card beats defense card
        # A card is beaten if its face value is higher, 
        # or if the defense card has the maximum face value and the attack card has the minimum face value
        if attack_card.value > defense_card.value:
            return True
        elif defense_card.value == 10 and attack_card.value == 1:  # Special rule
            return True
        return False
    
    def process_attack(self):
        if self.current_attack_card is None:
            if not self.draw_attack_card():
                return
        
        defending_player = self.get_defending_player()
        attacking_player = self.get_attacking_player()
        
        # Get current defense card
        defense_card = defending_player.team[self.current_defense_index]
        
        # Compare cards
        attack_wins = self.compare_cards(self.current_attack_card, defense_card)
        
        if attack_wins:
            # Attacker wins, card goes to attacker's deck
            self.game_message = f"Attack card {self.current_attack_card.value} beats defense card {defense_card.value}"
            attacking_player.deck.append(self.current_attack_card)
            attacking_player.deck.append(defense_card)
            
            # Mark defense card as beaten
            self.defense_index_beaten.append(self.current_defense_index)
            
            # Move to next defense card or score goal
            if self.current_defense_index == 3:  # Goalkeeper beaten
                self.game_message = f"GOAL! {attacking_player.name} scores!"
                attacking_player.goals += 1
                
                # Replace beaten defense cards
                self.reset_defense_cards()
                
                # Reset attack
                self.current_defense_index = 0
                self.defense_index_beaten = []
            else:
                self.current_defense_index += 1
                
                # Skip already beaten cards
                while self.current_defense_index in self.defense_index_beaten and self.current_defense_index < 4:
                    self.current_defense_index += 1
                    
            # Get new attack card
            self.current_attack_card = None
            
        else:
            # Defender wins, cards go to defender's deck
            self.game_message = f"Defense card {defense_card.value} blocks attack card {self.current_attack_card.value}"
            defending_player.deck.append(self.current_attack_card)
            defending_player.deck.append(defense_card)
            
            # Replace beaten defense cards
            self.reset_defense_cards()
            
            # Switch turns
            self.switch_turns()
            self.current_attack_card = None
    
    def reset_defense_cards(self):
        # Replace beaten defense cards including current defense index
        defending_player = self.get_defending_player()
        
        # Create new list for beaten indices
        indices_to_replace = self.defense_index_beaten.copy()
        if self.current_defense_index not in indices_to_replace:
            indices_to_replace.append(self.current_defense_index)
            
        # Sort indices to replace cards in correct order
        indices_to_replace.sort()
        
        # Replace cards
        for idx in indices_to_replace:
            if defending_player.deck:
                defending_player.team[idx] = defending_player.deck.pop(0)
    
    def draw(self):
        screen.fill(GREEN)
        
        # Draw teams
        self.player1.draw_team()
        self.player2.draw_team(True)
        
        # Draw decks
        self.player1.draw_deck(50, 500)
        self.player2.draw_deck(50, 100)
        
        # Draw current attack card if any
        if self.current_attack_card:
            self.current_attack_card.draw(SCREEN_WIDTH // 2 - CARD_WIDTH // 2, SCREEN_HEIGHT // 2 - CARD_HEIGHT // 2, True)
            
            # Draw arrow indicating attack direction
            target_y = 100 if self.player1.is_attacking else 500
            pygame.draw.line(screen, RED, 
                            (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), 
                            (250 + self.current_defense_index * (CARD_WIDTH + CARD_SPACING) + CARD_WIDTH//2, target_y + CARD_HEIGHT//2), 
                            3)
        
        # Draw game message
        message_text = font.render(self.game_message, True, BLACK)
        message_rect = message_text.get_rect(center=(SCREEN_WIDTH // 2, 30))
        screen.blit(message_text, message_rect)
        
        # Draw turn indicator
        turn_text = font.render(f"{'Player 1' if self.player1.is_attacking else 'Player 2'} is attacking", True, RED)
        turn_rect = turn_text.get_rect(center=(SCREEN_WIDTH // 2, 60))
        screen.blit(turn_text, turn_rect)
        
        # Draw instructions
        instructions = font.render("Press SPACE to draw attack card", True, BLACK)
        instructions_rect = instructions.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30))
        screen.blit(instructions, instructions_rect)

def main():
    game = Game()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game.process_attack()
                elif event.key == pygame.K_r:
                    # Reset game
                    game = Game()
                elif event.key == pygame.K_ESCAPE:
                    running = False
                    
        game.draw()
        pygame.display.flip()
        clock.tick(60)
        
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
