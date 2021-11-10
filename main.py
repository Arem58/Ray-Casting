from game import Game
g = Game()

while g.runnig:
    g.curr_menu.display_menu()
    g.game_loop()