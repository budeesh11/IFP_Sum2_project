from tempfootball import game
import pygame

g = game()

while g.running: #while the game is running
    g.curr_menu.display_menu()
    g.game_loop()
