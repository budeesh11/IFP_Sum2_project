#when done with game logic immplement this into the main football.py file

import pygame
import sys
from menu.menu import MainMenu, OptionsMenu, InstructionsMenu
from menu.game_interface import GameInterface

class game():
    def __init__(self):
        pygame.init()
        self.running, self.playing = True, False #running and playing state
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False #key states
        self.DISPLAY_W, self.DISPLAY_H = 1280, 720 #canvas size
        self.display = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H)) #creates a canvas
        self.window = pygame.display.set_mode((self.DISPLAY_W, self.DISPLAY_H)) #shows player what we are drawing
        self.font_name = None  # Using default system font
        self.font = pygame.font.Font(self.font_name, 32) #use default system font with size 32
        self.BLACK, self.WHITE, self.GREEN, self.RED, self.BLUE = (0, 0, 0), (255, 255, 255), (0, 100, 0), (200, 0, 0), (0, 0, 200) #colors
        # Load and scale background images
        self.background_image = pygame.image.load("menu/graphics/CardBall.png").convert()
        self.background_image = pygame.transform.scale(self.background_image, (self.DISPLAY_W, self.DISPLAY_H))
        self.field_image = pygame.image.load("menu/graphics/1.png").convert()
        self.field_image = pygame.transform.scale(self.field_image, (self.DISPLAY_W, self.DISPLAY_H))
        self.instructions_image = pygame.image.load("menu/graphics/Instructions.png").convert()
        self.instructions_image = pygame.transform.scale(self.instructions_image, (self.DISPLAY_W, self.DISPLAY_H))
        self.options_image = pygame.image.load("menu/graphics/Instructions (2).png").convert()
        self.options_image = pygame.transform.scale(self.options_image, (self.DISPLAY_W, self.DISPLAY_H))
        self.options_menu = OptionsMenu(self)
        self.instructions_menu = InstructionsMenu(self)
        self.main_menu = MainMenu(self)
        self.curr_menu = self.main_menu #current menu
        pygame.mixer.music.load("menu/sound/Dummy.mp3") #loads the music
        pygame.mixer.music.play(-1) #plays the music on loop
        pygame.mixer.music.set_volume(0.5) #sets the volume to 50% intially
        self.pause = False
        self.game_interface = None


    def game_loop(self): #performs the game functions
        while self.playing:
            if self.game_interface is None:
                # Initialize game interface when game starts
                self.game_interface = GameInterface(self)
                self.game_interface.run()
                self.game_interface = None  # Reset for next game
                self.playing = False
            else:
                self.check_events()
                if self.BACK_KEY:
                    self.playing = False #breaks the while loop without turning off the game
                if self.pause:
                    self.show_pause_menu()
                    continue  # Skip the loop if paused
                self.display.fill(self.BLACK) # Clear the screen first
                self.display.blit(self.field_image, (0, 0)) # Draw the field image
                self.window.blit(self.display, (0, 0)) #to align the display with the window
                pygame.display.update() #updates the screen
                self.reset() #resets the keys

    #checks for player input by going through a list of everything a player can input
    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                self.curr_menu.run_display = False #stops current menu from running
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
                if event.key == pygame.K_BACKSPACE:
                    self.pause = not self.pause
                if event.key == pygame.K_UP:
                    self.UP_KEY = True
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True

    def reset(self): #resets the keys after they have been clicked
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False

    #draws text on the screen
    def draw_text(self, text, size, color, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.display.blit(text_surface, text_rect)

    def draw_pause(self):
        # Draw a transparent overlay
        overlay = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H), pygame.SRCALPHA)
        overlay.fill((128, 128, 128, 150))
        self.display.blit(overlay, (0, 0))
        self.window.blit(self.display, (0, 0))
        pygame.display.update()

    def show_pause_menu(self):
        paused = True
        # Button rectangles
        button_width, button_height = 180, 50
        button_padding = 30
        center_x = self.DISPLAY_W // 2
        center_y = self.DISPLAY_H // 2
        # Main pause box
        box_width, box_height = 430, 250
        box_rect = pygame.Rect(center_x - box_width // 2, center_y - box_height // 2, box_width, box_height)
        # Reset button
        reset_rect = pygame.Rect(center_x - button_width - button_padding//2, center_y + 30, button_width, button_height)
        # Return button
        return_rect = pygame.Rect(center_x + button_padding//2, center_y + 30, button_width, button_height)
        font = pygame.font.Font(self.font_name, 36)
        small_font = pygame.font.Font(self.font_name, 28)
        while paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running, self.playing = False, False
                    paused = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        self.pause = False
                        paused = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if reset_rect.collidepoint(mouse_pos):
                        self.reset_game()  # Reset the game state
                        self.pause = False
                        paused = False
                    if return_rect.collidepoint(mouse_pos):
                        self.playing = False  # Exit game loop, return to main menu
                        self.pause = False
                        paused = False
                        if self.game_interface:
                            self.game_interface.running = False

            self.display.blit(self.field_image, (0, 0))
            # Draw transparent overlay
            overlay = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H), pygame.SRCALPHA)
            overlay.fill((128, 128, 128, 150))
            self.display.blit(overlay, (0, 0))
            # Draw main pause box
            pygame.draw.rect(self.display, (40, 40, 40), box_rect, border_radius=10)
            # Draw buttons
            pygame.draw.rect(self.display, (255, 255, 255), reset_rect, border_radius=10)
            pygame.draw.rect(self.display, (255, 255, 255), return_rect, border_radius=10)
            # Draw text
            text_paused = font.render("Game Paused", True, (255, 255, 255))
            text_resume = small_font.render("Backspace to resume", True, (200, 200, 200))
            text_reset = small_font.render("Reset", True, (0, 0, 0))
            text_return = small_font.render("Exit", True, (0, 0, 0))
            self.display.blit(text_paused, (center_x - text_paused.get_width() // 2, center_y - 80))
            self.display.blit(text_resume, (center_x - text_resume.get_width() // 2, center_y - 30))
            self.display.blit(text_reset, (reset_rect.centerx - text_reset.get_width() // 2, reset_rect.centery - text_reset.get_height() // 2))
            self.display.blit(text_return, (return_rect.centerx - text_return.get_width() // 2, return_rect.centery - text_return.get_height() // 2))
            self.window.blit(self.display, (0, 0))
            pygame.display.update()
            pygame.time.delay(50)

    def reset_game(self):
        # Reset the game state
        if self.game_interface:
            self.game_interface.initialize_game()
            # Reset the scores
            self.game_interface.player.goals = 0
            self.game_interface.computer.goals = 0
        else:
            # If game interface doesn't exist yet, just continue
            pass
