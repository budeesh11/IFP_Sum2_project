import pygame
import os

def create_card_back():
    # Initialize pygame
    pygame.init()
    
    # Card dimensions
    card_width = 80
    card_height = 120
    
    # Create a surface for the card back
    card_back = pygame.Surface((card_width, card_height))
    
    # Fill with dark blue background
    card_back.fill((0, 0, 100))
    
    # Draw a pattern
    for i in range(0, card_width, 10):
        for j in range(0, card_height, 10):
            if (i + j) % 20 == 0:
                pygame.draw.rect(card_back, (0, 0, 150), (i, j, 10, 10))
    
    # Draw a border
    pygame.draw.rect(card_back, (200, 200, 200), (0, 0, card_width, card_height), 2)
    
    # Draw a central design
    pygame.draw.circle(card_back, (200, 200, 200), (card_width // 2, card_height // 2), 20)
    pygame.draw.circle(card_back, (0, 0, 100), (card_width // 2, card_height // 2), 15)
    
    # Save the image
    pygame.image.save(card_back, "menu/assets/card_back.png")
    print("Card back created successfully!")

if __name__ == "__main__":
    create_card_back() 