from tempfootball import game

g = game()

while g.running: #while the game is running
    g.playing = True
    g.game_loop()
