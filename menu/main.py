from menu.game_manager import game
import pygame

g = game()

while g.running:
    g.curr_menu.display_menu()
    g.game_loop()