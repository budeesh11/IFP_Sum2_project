#5660585
import pygame
import sys

class menu():
    def __init__(self, game):
        self.game = game #gives access to the game class
        self.mid_w, self.mid_h = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2
        self.surface = pygame.Surface((self.game.DISPLAY_W, self.game.DISPLAY_H), pygame.SRCALPHA)
        self.run_display = True #runs the display
        self.cursor_rect = pygame.Rect(0, 0, 400, 50)  
        self.offset = -200
        self.selected_color = self.game.RED  # Color for selected option
        self.unselected_color = (50, 50, 50)  # Dark gray for unselected options

    def display_controls(self, surface, controls):
        color = (255, 255, 255) if self.selected else (255, 250, 239)
        pygame.draw.rect(surface, color, (80, 270/4 - 10 + (self.curr_index*30), 320, 20))
        i = 0
        for control in controls:
            self.game.draw_text(control + '-' + pygame.key.name(controls[control]), 
                              20, pygame.Color(0, 0, 0), 480 / 2, 270/4 + i)
            i += 30

    def draw_cursor(self): #draws the cursor
        pygame.draw.rect(self.game.display, self.selected_color, self.cursor_rect)

    def blit_screen(self):
        self.game.window.blit(self.game.display, (0, 0)) #blits the screen
        pygame.display.update() #updates the display
        self.game.reset() #resets the keys

class MainMenu(menu): #inherits the base class menu
    def __init__(self, game):
        menu.__init__(self, game) #to use the init function that we made for the base menu class
        self.state = "Start" #to keep track of current state
        self.startx, self.starty = self.mid_w, self.mid_h + 40
        self.optionsx, self.optionsy = self.mid_w, self.mid_h + 120
        self.instructionsx, self.instructionsy = self.mid_w, self.mid_h + 200 
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty - 15)

    def display_menu(self): #function to display the menu
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.blit(self.game.background_image, (0, 0))
            
            # background rectangles
            start_rect = pygame.Rect(self.startx + self.offset, self.starty - 23, 400, 50)
            options_rect = pygame.Rect(self.optionsx + self.offset, self.optionsy - 23, 400, 50)
            instructions_rect = pygame.Rect(self.instructionsx + self.offset, self.instructionsy - 15, 400, 50)
            
            # background for unselected options
            pygame.draw.rect(self.game.display, self.unselected_color, start_rect)
            pygame.draw.rect(self.game.display, self.unselected_color, options_rect)
            pygame.draw.rect(self.game.display, self.unselected_color, instructions_rect)
            
            # background for selected option
            if self.state == "Start":
                pygame.draw.rect(self.game.display, self.selected_color, start_rect)
            elif self.state == "Options":
                pygame.draw.rect(self.game.display, self.selected_color, options_rect)
            elif self.state == "Instructions":
                pygame.draw.rect(self.game.display, self.selected_color, instructions_rect)
            
            self.game.draw_text("Start Game", 36, self.game.WHITE, self.startx, self.starty)
            self.game.draw_text("Options", 36, self.game.WHITE, self.optionsx, self.optionsy)
            self.game.draw_text("Instructions", 36, self.game.WHITE, self.instructionsx, self.instructionsy)
            self.blit_screen()

    def move_cursor(self): #function to move the cursor between the options
        if self.game.DOWN_KEY:
            if self.state == "Start":
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy - 15)
                self.state = "Options"
            elif self.state == "Options":
                self.cursor_rect.midtop = (self.instructionsx + self.offset, self.instructionsy - 15)
                self.state = "Instructions"
            elif self.state == "Instructions":
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty - 15)
                self.state = "Start"
        elif self.game.UP_KEY:
            if self.state == "Start":
                self.cursor_rect.midtop = (self.instructionsx + self.offset, self.instructionsy - 15)
                self.state = "Instructions"
            elif self.state == "Options":
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty - 15)
                self.state = "Start"
            elif self.state == "Instructions":
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy - 15)
                self.state = "Options"

    def check_input(self): #function to check the input
        self.move_cursor() #checks if the player want to move the cursor
        if self.game.START_KEY:
            if self.state == "Start":
                self.game.playing = True
            elif self.state == "Options":
                self.game.curr_menu = self.game.options_menu
            elif self.state == "Instructions":
                self.game.curr_menu = self.game.instructions_menu
            self.run_display = False #closes the menu

class VolumeSlider: #configuring the volume slider
    def __init__(self, game, pos: tuple, size: tuple, initial_value: float):
        self.game = game
        self.pos = pos
        self.size = size

        self.slider_left_pos = self.pos[0] - self.size[0] // 2
        self.slider_right_pos = self.pos[0] + self.size[0] // 2
        self.slider_top_pos = self.pos[1] - self.size[1] // 2

        self.value = initial_value
        self.dragging = False

        self.container_rect = pygame.Rect(self.slider_left_pos, self.slider_top_pos, self.size[0], self.size[1])
        self.button_rect = pygame.Rect(self.slider_left_pos + (self.size[0] * initial_value) - 10, 
                                     self.slider_top_pos - 5, 20, self.size[1] + 10)

    def render(self, screen):
        # Draw track
        pygame.draw.rect(screen, (100, 100, 100), self.container_rect, border_radius=3)
        
        # Draw filled portion
        filled_width = int(self.size[0] * self.value)
        filled_rect = pygame.Rect(self.slider_left_pos, self.slider_top_pos, filled_width, self.size[1])
        pygame.draw.rect(screen, (50, 150, 255), filled_rect, border_radius=3)
        
        # Draw slider button
        button_color = (220, 220, 220) if self.dragging else (200, 200, 200)
        pygame.draw.rect(screen, button_color, self.button_rect, border_radius=5)
        
        # Draw border around button
        pygame.draw.rect(screen, (80, 80, 80), self.button_rect, width=2, border_radius=5)

    def update_button_position(self):
        # Update button position based on current value
        self.button_rect.x = self.slider_left_pos + (self.size[0] * self.value) - 10

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
            # Get raw mouse position
            mouse_pos = pygame.mouse.get_pos()
            
            # Create a rect for checking collision
            check_rect = pygame.Rect(
                self.button_rect.x * self.game.window.get_width() / self.game.DISPLAY_W,
                self.button_rect.y * self.game.window.get_height() / self.game.DISPLAY_H,
                self.button_rect.width * self.game.window.get_width() / self.game.DISPLAY_W,
                self.button_rect.height * self.game.window.get_height() / self.game.DISPLAY_H
            )
            
            # Check if click is on button
            if check_rect.collidepoint(mouse_pos):
                self.dragging = True
                return True
                
            # Check if click is on slider track
            check_track = pygame.Rect(
                self.container_rect.x * self.game.window.get_width() / self.game.DISPLAY_W,
                self.container_rect.y * self.game.window.get_height() / self.game.DISPLAY_H,
                self.container_rect.width * self.game.window.get_width() / self.game.DISPLAY_W,
                self.container_rect.height * self.game.window.get_height() / self.game.DISPLAY_H
            )
            
            if check_track.collidepoint(mouse_pos):
                self.dragging = True
                # Update value based on click position
                rel_x = (mouse_pos[0] - check_track.x) / check_track.width
                self.value = max(0, min(1, rel_x))
                self.update_button_position()
                return True
                
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.dragging:
                self.dragging = False
                return True
                
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            mouse_pos = pygame.mouse.get_pos()
            
            # Calculate track position in window coordinates
            track_x = self.slider_left_pos * self.game.window.get_width() / self.game.DISPLAY_W
            track_width = self.size[0] * self.game.window.get_width() / self.game.DISPLAY_W
            
            # Calculate relative position
            rel_x = (mouse_pos[0] - track_x) / track_width
            self.value = max(0, min(1, rel_x))
            self.update_button_position()
            return True
            
        return False

class OptionsMenu(menu): #options menu
    def __init__(self, game):
        menu.__init__(self, game)
        self.state = "Volume"
        self.volx, self.voly = self.mid_w, self.mid_h - 40
        self.cursor_rect.midtop = (self.volx + self.offset, self.voly - 15)
        
        # Set initial volume (default to 0.5 if not set)
        try:
            initial_volume = pygame.mixer.music.get_volume()
        except:
            initial_volume = 0.5
            
        self.volume_slider = VolumeSlider(
            game=self.game,
            pos=(self.mid_w + 60, self.mid_h + 20),
            size=(200, 20),
            initial_value=initial_volume
        )

    def display_menu(self): #displaying the menu
        self.run_display = True
        while self.run_display:
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.display.blit(self.game.options_image, (0, 0))
            
            #background rectangle
            volume_rect = pygame.Rect(self.volx + self.offset, self.voly - 15, 400, 50)
            
            #volume option highlight
            pygame.draw.rect(self.game.display, self.selected_color, volume_rect)
            
            self.game.draw_text("Volume", 36, self.game.WHITE, self.volx, self.voly)
            
            # Draw slider and volume percentage
            self.volume_slider.render(self.game.display)
            
            volume_percentage = int(self.volume_slider.value * 100)
            self.game.draw_text(f"{volume_percentage}%", 36, self.game.WHITE, 
                              self.mid_w - 160, self.mid_h + 20)
            
            self.blit_screen()

    def check_input(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # Handle slider events
            if self.volume_slider.handle_event(event):
                try:
                    pygame.mixer.music.set_volume(self.volume_slider.value)
                except:
                    pass  # Music might not be initialized
                continue
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.game.curr_menu = self.game.main_menu
                    self.run_display = False
                elif event.key == pygame.K_LEFT:
                    self.volume_slider.value = max(0, self.volume_slider.value - 0.05)
                    self.volume_slider.update_button_position()
                    try:
                        pygame.mixer.music.set_volume(self.volume_slider.value)
                    except:
                        pass
                elif event.key == pygame.K_RIGHT:
                    self.volume_slider.value = min(1, self.volume_slider.value + 0.05)
                    self.volume_slider.update_button_position()
                    try:
                        pygame.mixer.music.set_volume(self.volume_slider.value)
                    except:
                        pass

class InstructionsMenu(menu): #instructions menu
    def __init__(self, game):
        menu.__init__(self, game)

    def display_menu(self): 
        self.run_display = True
        while self.run_display:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        self.game.curr_menu = self.game.main_menu
                        self.run_display = False
            self.game.display.fill(self.game.BLACK)
            self.game.display.blit(self.game.instructions_image, (0, 0))
            self.blit_screen()
#5660585