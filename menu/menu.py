import pygame
import sys

class menu():
    def __init__(self, game):
        self.game = game #gives access to the game class
        self.mid_w, self.mid_h = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2
        self.run_display = True #runs the display
        self.cursor_rect = pygame.Rect(0, 0, 50, 50) #cursor
        self.offset = -100 #puts the cursor to the left of the buttons

    def draw_cursor(self):
        self.game.draw_text('*', 15, self.game.WHITE, self.cursor_rect.x, self.cursor_rect.y) #draws the cursor

    def blit_screen(self):
        self.game.window.blit(self.game.display, (0, 0)) #blits the screen
        pygame.display.update() #updates the display
        self.game.reset() #resets the keys

class MainMenu(menu): #inherits the base class menu
    def __init__(self, game):
        menu.__init__(self, game) #to use the init function that we made for the base menu class
        self.state = "Start" #to keep track of current state
        self.startx, self.starty = self.mid_w, self.mid_h + 40
        self.optionsx, self.optionsy = self.mid_w, self.mid_h + 120  # 80px separation
        self.instructionsx, self.instructionsy = self.mid_w, self.mid_h + 200  # 80px separation
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty) #cursor starting position

    def display_menu(self): #function to display the menu
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.blit(self.game.background_image, (0, 0))
            self.game.draw_text("Start Game", 36, self.game.WHITE, self.startx, self.starty)
            self.game.draw_text("Options", 36, self.game.WHITE, self.optionsx, self.optionsy)
            self.game.draw_text("Instructions", 36, self.game.WHITE, self.instructionsx, self.instructionsy)
            self.draw_cursor()
            self.blit_screen()

    def move_cursor(self): #function to move the cursor between the options
        if self.game.DOWN_KEY:
            if self.state == "Start":
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = "Options"
            elif self.state == "Options":
                self.cursor_rect.midtop = (self.instructionsx + self.offset, self.instructionsy)
                self.state = "Instructions"
            elif self.state == "Instructions":
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = "Start"
        elif self.game.UP_KEY:
            if self.state == "Start":
                self.cursor_rect.midtop = (self.instructionsx + self.offset, self.instructionsy)
                self.state = "Instructions"
            elif self.state == "Options":
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = "Start"
            elif self.state == "Instructions":
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = "Options"

    def check_input(self): #function to check the input
        self.move_cursor() #checks if the player want to move the cursor
        if self.game.START_KEY:
            if self.state == "Start":
                self.game.playing = True
            elif self.state == "Options": #switch to the options menu
                self.game.curr_menu = self.game.options_menu
            elif self.state == "Instructions": #switch to the instructions menu
                self.game.curr_menu = self.game.instructions_menu
            self.run_display = False #closes the menu

class OptionsMenu(menu): #options menu
    def __init__(self, game):
        menu.__init__(self, game)
        self.state = "Volume"
        self.volx, self.voly = self.mid_w, self.mid_h + 20
        self.controlsx, self.controlsy = self.mid_w, self.mid_h + 70
        self.cursor_rect.midtop = (self.volx + self.offset, self.voly)

    def display_menu(self): #function to display the menu
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.display.blit(self.game.options_image, (0, 0))  # Draw the options background
            self.game.draw_text("Volume", 18, self.game.WHITE, self.volx, self.voly)
            self.game.draw_text("Controls", 18, self.game.WHITE, self.controlsx, self.controlsy)
            self.draw_cursor()
            self.blit_screen()

    def check_input(self): #function to go back to the main menu
        if self.game.BACK_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False #breaks the while loop
        elif self.game.UP_KEY or self.game.DOWN_KEY:
            if self.state == "Volume":
                self.state = "Controls"
                self.cursor_rect.midtop = (self.controlsx + self.offset, self.controlsy)
            elif self.state == "Controls":
                self.state = "Volume"
                self.cursor_rect.midtop = (self.volx + self.offset, self.voly)
        elif self.game.START_KEY:
            #add volume change here
            pass

class InstructionsMenu(menu): #instructions menu
    def __init__(self, game):
        menu.__init__(self, game)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            if self.game.START_KEY or self.game.BACK_KEY:
                self.game.curr_menu = self.game.main_menu
                self.run_display = False
            self.game.display.fill(self.game.BLACK)
            self.game.display.blit(self.game.instructions_image, (0, 0))
            self.blit_screen()











            


        
        
            
        
